from flask import Flask, render_template, request, send_file
import os
import cv2
import numpy as np
import joblib
import pandas as pd
from collections import Counter
from utils.drive_downloader import download_images_from_drive

app = Flask(__name__)
UPLOAD_FOLDER = 'static/downloads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load soil type prediction model
soil_model = joblib.load("models/soil_type_model.pkl")

# Mapping from predicted index to soil type names
soil_label_map = {
    0: "Red Soil",
    1: "Black Soil",
    2: "Alluvial Soil",
    3: "Laterite Soil",
    4: "Sandy Soil",
    5: "Peaty Soil",
    6: "Clay Soil"
}

# Extracts color features from the image
def extract_features(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (224, 224))

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    rgb_mean = np.mean(rgb, axis=(0, 1))
    hsv_mean = np.mean(hsv, axis=(0, 1))
    lab_mean = np.mean(lab, axis=(0, 1))

    rgb_std = np.std(rgb, axis=(0, 1))
    hsv_std = np.std(hsv, axis=(0, 1))
    lab_std = np.std(lab, axis=(0, 1))

    features = np.concatenate([rgb_mean, hsv_mean, lab_mean, rgb_std, hsv_std, lab_std])
    return features.reshape(1, -1), rgb_mean, hsv_mean, lab_mean

# Determines soil condition based on brightness
def get_condition_from_rgb(rgb_mean):
    r, g, b = rgb_mean
    brightness = np.mean([r, g, b])
    if brightness > 180:
        return "Dry"
    elif brightness > 100:
        return "Good"
    elif brightness > 60:
        return "Wet"
    else:
        return "Bad"

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    summary = {}

    if request.method == "POST":
        folder_id = request.form["folder_id"]
        downloaded_files = download_images_from_drive(folder_id, UPLOAD_FOLDER)

        for file_path in downloaded_files:
            features, rgb_mean, hsv_mean, lab_mean = extract_features(file_path)
            soil_index = soil_model.predict(features)[0]
            soil_type = soil_label_map.get(soil_index, f"Class {soil_index}")
            condition = get_condition_from_rgb(rgb_mean)

            r, g, b = np.round(rgb_mean, 2)
            h, s, v = np.round(hsv_mean, 2)
            l, a, b_lab = np.round(lab_mean, 2)

            results.append({
                "filename": os.path.basename(file_path),
                "soil_type": soil_type,
                "condition": condition,
                "RGB": f"R:{r}, G:{g}, B:{b}",
                "HSV": f"H:{h}, S:{s}, V:{v}",
                "LAB": f"L:{l}, A:{a}, B:{b_lab}"
            })

        # Generate summary
        soil_counts = Counter([r["soil_type"] for r in results])
        condition_counts = Counter([r["condition"] for r in results])
        summary = {
            "soil_counts": dict(soil_counts),
            "condition_counts": dict(condition_counts)
        }

        # Save to CSV
        df = pd.DataFrame(results, columns=["filename", "soil_type", "condition", "RGB", "HSV", "LAB"])
        df.to_csv("static/report.csv", index=False)

    return render_template("index.html", results=results, summary=summary)

@app.route("/download_report")
def download_report():
    return send_file("static/report.csv", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
