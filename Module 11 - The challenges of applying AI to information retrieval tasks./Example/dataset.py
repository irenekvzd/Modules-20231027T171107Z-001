from sklearn.datasets import fetch_20newsgroups

# Fetch the dataset
newsgroups = fetch_20newsgroups(subset='all')
data, target = newsgroups.data, newsgroups.target
