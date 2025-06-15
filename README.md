# 🌱 Soil Color Analyzer – ML Web App

A machine learning–powered web application that predicts **soil type** and **fertility class** from an image of soil. Built using Python, Flask, and HTML/CSS, the app allows users to upload a soil image and get instant feedback on soil quality.

🔍 Features

- 🌾 Predicts **soil type** (e.g., Black, Clay, Red, Alluvial)
- ✅ Maps soil type to **fertility class** (Rich, Moderate, Poor)
- 📷 Accepts image input via file upload
- 💡 Clean UI with modern CSS animations
- 💾 Trained using extracted color features (RGB, HSV, Lab)
- ⚡ Fast predictions using a pre-trained Random Forest model

📁 Project Structure

soil_color_analyzer/
├── app/
│   ├── app.py                    # Flask backend
│   ├── templates/
│   │   └── index.html            # Upload form UI
│   └── static/
│       ├── style.css             # CSS styling
│       └── logo.png              # Optional logo
├── data/
│   ├── raw/                      # Raw images (optional)
│   └── processed/
│       └── soil_color_features.csv
├── models/
│   ├── soil_type_model.pkl       # Trained classifier
│   └── soil_label_encoder.pkl    # Label encoder for soil types
├── notebooks/
│   └── EDA_Feature_Extraction.ipynb
├── utils/
│   └── preprocessing.py          # Feature extraction script
├── requirements.txt              # Python dependencies
└── README.md

---

🚀 How to Run Locally

1. 📦 Install Dependencies

Make sure you have Python 3.8+ installed.

pip install -r requirements.txt

2. 🤖 Train the Model (Optional)

If you don't have the model files:

python train_model.py

3. ▶️ Launch the App

cd app  
python app.py

Then open your browser at:  
📍 http://127.0.0.1:5000/


 🧠 How It Works

1. User uploads a soil image.
2. App extracts color features (mean/std of RGB, HSV, Lab).
3. Model predicts soil type.
4. App maps it to fertility class and displays the result.


 🌐 Tech Stack

- Python 🐍  
- Flask 🌐  
- OpenCV + Pillow (Image Processing) 🖼️  
- Scikit-learn (ML) 🤖  
- HTML/CSS (Frontend) 🎨  

📌 Future Improvements

- Add pH and nutrient prediction
- Mobile-responsive UI
- Streamlit or Gradio version
- Support for real-time webcam input
