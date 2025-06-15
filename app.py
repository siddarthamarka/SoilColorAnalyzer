from flask import Flask, render_template, request
from PIL import Image
import numpy as np
import cv2
import joblib
import os

app = Flask(__name__)

IMG_SIZE = (224, 224)

# Load models and encoders
soil_model = joblib.load("../models/soil_type_model.pkl")
soil_encoder = joblib.load("../models/soil_label_encoder.pkl")
fertility_map = joblib.load("../models/fertility_map.pkl")

def extract_features(image):
    image = image.convert('RGB').resize(IMG_SIZE)
    img_np = np.array(image)
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    lab = cv2.cvtColor(img_np, cv2.COLOR_RGB2Lab)
    
    features = []
    for i in range(3):
        features.append(img_np[:, :, i].mean())
        features.append(img_np[:, :, i].std())
    for i in range(3):
        features.append(hsv[:, :, i].mean())
        features.append(hsv[:, :, i].std())
    for i in range(3):
        features.append(lab[:, :, i].mean())
        features.append(lab[:, :, i].std())
    return np.array(features).reshape(1, -1)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        file = request.files["image"]
        if file:
            image = Image.open(file.stream)
            features = extract_features(image)
            soil_pred = soil_model.predict(features)[0]
            soil_type = soil_encoder.inverse_transform([soil_pred])[0]
            fertility = fertility_map.get(soil_type, "Unknown")
            result = f"Predicted Soil Type: <strong>{soil_type}</strong><br>Predicted Fertility Class: <strong>{fertility}</strong>"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)