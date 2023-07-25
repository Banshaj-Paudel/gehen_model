from flask import Flask, request, jsonify
from model import predict_dementia
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    try:
        # Check if the request contains an image
        if 'image' not in request.files:
            return jsonify({'error': 'No image sent'}), 400

        image_file = request.files['image']
        # Save the image to a temporary location on the server
        image_path = 'temp_image.jpg'
        image_file.save(image_path)

        # Make a prediction using the uploaded image
        predicted_class, percent_chances = predict_dementia(image_path)

        # Delete the temporary image file
        os.remove(image_path)

        return jsonify({'predicted_class': predicted_class, 'percent_chances': percent_chances}), 200

    except Exception as e:
        print("Error:", e)  # Debug statement
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
