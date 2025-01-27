from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np

# Load the trained model
model = tf.keras.models.load_model("models/trans_model.h5")

# Create a Flask app
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to the Iris Prediction API! Use the /predict endpoint to make predictions.",
        "usage": "/predict?sepal_length=<value>&sepal_width=<value>&petal_length=<value>&petal_width=<value>"
    }), 200

# Define a route for predictions
@app.route('/predict', methods=['GET'])
def predict():
    # Extract query parameters for model input
    try:
        sepal_length = float(request.args.get('sepal_length'))
        sepal_width = float(request.args.get('sepal_width'))
        petal_length = float(request.args.get('petal_length'))
        petal_width = float(request.args.get('petal_width'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid input. Provide numeric values for all features."}), 400

    # Prepare input data
    input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

    # Make prediction
    prediction = model.predict(input_data)
    predicted_class = np.argmax(prediction, axis=1)[0]
    class_probabilities = prediction[0].tolist()

    # Map predicted class to Iris species
    iris_classes = ['setosa', 'versicolor', 'virginica']
    species = iris_classes[predicted_class]

    # Return prediction as JSON
    response = {
        "predicted_class": species,
        "class_probabilities": {
            iris_classes[0]: class_probabilities[0],
            iris_classes[1]: class_probabilities[1],
            iris_classes[2]: class_probabilities[2]
        }
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)