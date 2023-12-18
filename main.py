from flask import Flask, request, jsonify
from keras.models import load_model
from PIL import Image
import requests
from io import BytesIO
import numpy as np
from bird_class import bird_classes

app = Flask(__name__)
model = None


def load_custom_model():
    global model
    model = load_model("./Mobinet.h5")


@app.route("/")
def hello_world():
    return "<p>API for prediction bird !</p>"


@app.route("/predict", methods=["POST"])
def predict():
    global model

    if model is None:
        load_custom_model()

    file = request.files['file']
    image = Image.open(file)

    image = image.resize((224, 224))
    image = np.expand_dims(image, axis=0)
    image = image / 255.0
    
    try:

        prediction = model.predict(image)

        # Get the indices of the top 5 predictions
        top_indices = np.argsort(prediction[0])[::-1][:5]

        top_predictions = [
                    {
                        "predicted_id": int(idx + 1),
                        "confidence": round(100 * prediction[0][idx], 2),
                        "class_name": bird_classes[idx],
                    }
                    for idx in top_indices
                ]

        return jsonify(top_predictions)
    except Exception as e:
        return jsonify(error=str(e))


if __name__ == "__main__":
    app.run(debug=True, port = 5000)
