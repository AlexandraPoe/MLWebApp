from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os

# Get the current directory of app.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define paths for templates, static, and models
template_dir = os.path.join(current_dir, "templates")
static_dir = os.path.join(current_dir, "static")
model_dir = os.path.join(current_dir, "models")

# Initialize Flask app
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Paths to models
regression_model_path = os.path.join(model_dir, "best_regression_model..pkl")
classification_model_path = os.path.join(model_dir, "best_classification_model..pkl")

# Verify model files exist
if not os.path.exists(regression_model_path) or not os.path.exists(classification_model_path):
    raise FileNotFoundError("Model files are missing! Ensure both regression and classification models exist.")

# Load models
regression_model = joblib.load(regression_model_path)
classification_model = joblib.load(classification_model_path)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict_regression", methods=["POST"])
def predict_regression():
    try:
        data = request.json
        print("Received data for regression:", data)

        # Validate inputs
        required_keys = ['vendor_label', 'model_label', 'myct', 'mmin', 'mmax', 'cach', 'chmin', 'chmax']
        if not all(key in data for key in required_keys):
            raise ValueError("Missing one or more required input fields.")

        # Convert input to numerical types
        features = np.array([[float(data['vendor_label']), float(data['model_label']), float(data['myct']),
                              float(data['mmin']), float(data['mmax']), float(data['cach']),
                              float(data['chmin']), float(data['chmax'])]])
        print("Features for regression:", features)
        print("Received data for regression:", data)
        prediction = regression_model.predict(features)[0]
        print("Regression prediction result:", prediction)
        return jsonify({"ERP Prediction": prediction})
    except Exception as e:
        print("Error in regression prediction:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/predict_classification", methods=["POST"])
def predict_classification():
    try:
        data = request.json
        print("Received data for classification:", data)

        # Convert input to numerical types
        features = np.array([[float(data['vendor_label']), float(data['model_label']), float(data['myct']),
                              float(data['mmin']), float(data['mmax']), float(data['cach']),
                              float(data['chmin']), float(data['chmax'])]])
        print("Features for classification:", features)

        prediction = classification_model.predict(features)[0]
        print("Classification prediction result:", prediction)

        label = "High Performance" if prediction == 1 else "Low Performance"
        return jsonify({"Performance Prediction": label})
    except Exception as e:
        print("Error in classification prediction:", str(e))
        return jsonify({"error": str(e)}), 500

# Load models with debug logging
try:
    regression_model = joblib.load(regression_model_path)
    print("Regression model loaded successfully.")
except Exception as e:
    print(f"Error loading regression model: {e}")

try:
    classification_model = joblib.load(classification_model_path)
    print("Classification model loaded successfully.")
except Exception as e:
    print(f"Error loading classification model: {e}")


if __name__ == "__main__":
    app.run(debug=True)
