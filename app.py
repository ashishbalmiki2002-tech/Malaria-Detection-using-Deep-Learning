import json
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Mock mode flag - set to False when TensorFlow is available
MOCK_MODE = False
classes = {0: 'Parasitized', 1: 'Uninfected'}

# Load the model - try different methods for compatibility
model = None

if not MOCK_MODE:
    try:
        # Try loading with keras 3
        import keras
        model = keras.saving.load_model('models/CNN.h5')
        print("Model loaded successfully with Keras 3")
    except Exception as e:
        print(f"Error loading model with Keras 3: {e}")
        try:
            # Fallback to legacy loading
            from keras.models import load_model
            model = load_model('models/CNN.h5', compile=False)
            print("Model loaded successfully with legacy method")
        except Exception as e2:
            print(f"Error loading model with legacy method: {e2}")
            print("Switching to MOCK MODE for testing")
            MOCK_MODE = True
else:
    print("Running in MOCK MODE - predictions will be simulated")

with open("config.json", "r") as c:
    params = json.load(c)["params"]


@app.route("/")
def landingPage():
    return render_template("index.html")


@app.route("/form")
def inputForm():
    return render_template("form.html")


@app.route("/result")
def result():
    return render_template("result.html")


@app.route("/predict", methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(url_for('inputForm'))
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(url_for('inputForm'))
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            if MOCK_MODE:
                # Mock prediction based on simple image analysis
                img = cv2.imread(filepath)
                
                # Simple heuristic: analyze average color intensity
                # This is just for testing - not real malaria detection!
                avg_color = np.mean(img)
                
                # Simulate prediction based on brightness
                if avg_color < 120:
                    index = 0  # Parasitized (darker images)
                    certainty = 75.0 + np.random.uniform(0, 20)
                else:
                    index = 1  # Uninfected (brighter images)
                    certainty = 70.0 + np.random.uniform(0, 25)
                
                result_class = classes[index]
                
                print(f"MOCK PREDICTION: {result_class} with {certainty:.2f}% certainty")
                
            else:
                # Real model prediction
                img = cv2.imread(filepath)
                img = cv2.resize(img, (50, 50))
                img = img.reshape(-1, 50, 50, 3)
                img = img / 255.0
                
                # Make prediction
                prd = model.predict(img, verbose=0)
                certainty = np.amax(prd) * 100
                index = prd.argmax()
                
                result_class = classes[index]
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return render_template("result.html", 
                                 prediction=result_class, 
                                 certainty=f"{certainty:.2f}",
                                 mock_mode=MOCK_MODE)
        except Exception as e:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
            return render_template("result.html", 
                                 prediction="Error", 
                                 certainty=f"Processing failed: {str(e)}")
    
    return redirect(url_for('inputForm'))


@app.route("/team")
def team():
    return render_template("team.html", params=params)


@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):

    return render_template("404.html")


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except:
        print("Error")
