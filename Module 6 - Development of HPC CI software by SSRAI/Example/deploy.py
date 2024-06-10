from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model

app = Flask(__name__)

model = load_model('path/to/saved_model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    img = request.files['image']
    img_tensor = load_image(img)
    pred = model.predict(img_tensor)
    return jsonify({'prediction': str(pred)})

if __name__ == '__main__':
    app.run(debug=True)
