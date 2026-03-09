# Malaria-Detection-using-Deep-Learning

📌 Overview
This project applies Convolutional Neural Networks (CNNs) and Transfer Learning to detect malaria parasites in microscopic blood smear images. It provides a scalable, automated solution to assist healthcare professionals in early diagnosis.

📂 Repository Structure
Code
Malaria-Detection-using-Deep-Learning/
│
├── Documentation/       # Project reports, references, and supporting docs
├── Notebooks/           # Jupyter notebooks for experiments & training
├── holdout_dataset/     # Validation dataset (Parasitized/Uninfected images)
├── models/              # Saved trained models (.h5, checkpoints)
├── script/              # Python scripts for preprocessing & training
├── static/              # Static assets (CSS, JS, images for Flask app)
├── templates/           # HTML templates for Flask web interface
├── tests/               # Unit tests for model and app
│
├── app.py               # Flask application entry point
├── config.json          # Configuration settings
├── requirements.txt     # Python dependencies
├── run.bat              # Windows batch file for quick execution
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
🚀 Features
Automated classification: Parasitized vs. Uninfected

Models: Custom CNN, MobileNetV2, EfficientNetB0

Flask-based web interface for predictions

Confidence score display

Modular structure for easy extension

⚙️ Installation
Clone the repository and install dependencies:

bash
git clone https://github.com/ashishbalmiki2002-tech/Malaria-Detection-using-Deep-Learning.git
cd Malaria-Detection-using-Deep-Learning
pip install -r requirements.txt
▶️ Usage
Run the Flask app:

bash
python app.py
Or on Windows:

bash
run.bat
Then open http://127.0.0.1:5000/ in your browser to upload blood smear images and get predictions.

📊 Workflow
Data Preprocessing – Resize, normalize, augment images

Model Training – CNN + Transfer Learning

Evaluation – Accuracy, Precision, Recall, ROC AUC

Deployment – Flask web app for real-time predictions

https://drive.google.com/file/d/1EKYOYutfVYOlCKkaHypapAKj3tF7a-N5/view?usp=sharing

demo video link for this app 👆
