import os
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import horovod.torch as hvd
from tqdm import tqdm
import time

# Initialize Horovod
hvd.init()
torch.cuda.set_device(hvd.local_rank())

# Hyperparameters
batch_size = 64
num_epochs = 10
learning_rate = 0.01

# Data Loading
def get_data_loader(data_dir, batch_size, train=True):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    dataset = datasets.CIFAR10(root=data_dir, train=train, transform=transform, download=True)
    sampler = data.distributed.DistributedSampler(dataset, num_replicas=hvd.size(), rank=hvd.rank())
    loader = data.DataLoader(dataset, batch_size=batch_size, sampler=sampler, num_workers=4)
    
    return loader

# Model Definition
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.fc1 = nn.Linear(128 * 8 * 8, 256)
        self.fc2 = nn.Linear(256, 10)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 128 * 8 * 8)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Training Function
def train(epoch, model, train_loader, optimizer, criterion):
    model.train()
    train_loader.sampler.set_epoch(epoch)
    running_loss = 0.0
    total = 0
    correct = 0
    for batch_idx, (inputs, targets) in enumerate(tqdm(train_loader)):
        inputs, targets = inputs.cuda(), targets.cuda()
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
        
    print(f"Epoch {epoch}, Loss: {running_loss/len(train_loader)}, Accuracy: {100.*correct/total}")

# Main Function
def main():
    # Horovod: limit CPU threads to be used per worker.
    torch.set_num_threads(4)
    
    data_dir = './data'
    train_loader = get_data_loader(data_dir, batch_size, train=True)
    test_loader = get_data_loader(data_dir, batch_size, train=False)
    
    model = SimpleCNN().cuda()
    
    # Horovod: scale learning rate by the number of GPUs.
    optimizer = optim.SGD(model.parameters(), lr=learning_rate * hvd.size(), momentum=0.9, weight_decay=5e-4)
    
    # Horovod: broadcast parameters & optimizer state.
    hvd.broadcast_parameters(model.state_dict(), root_rank=0)
    hvd.broadcast_optimizer_state(optimizer, root_rank=0)
    
    # Horovod: wrap optimizer with DistributedOptimizer.
    optimizer = hvd.DistributedOptimizer(optimizer, named_parameters=model.named_parameters())
    
    criterion = nn.CrossEntropyLoss().cuda()
    
    for epoch in range(1, num_epochs + 1):
        train(epoch, model, train_loader, optimizer, criterion)
    
    print("Training complete")

if __name__ == '__main__':
    main()
