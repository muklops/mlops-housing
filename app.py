import os
import sys
import pickle
import boto3
from flask import Flask, request, jsonify

from src.logger.logger import logger
from src.exception.exception import CustomException


# -------------------- App Init --------------------
app = Flask(__name__)

S3_BUCKET = "housingmk"
S3_MODEL_KEY = "model/model.pkl"
LOCAL_MODEL_PATH = "model.pkl"


def load_model():
    """
    Download model from S3 and load into memory
    """
    try:
        logger.info(
            f"Downloading model from s3://{S3_BUCKET}/{S3_MODEL_KEY}"
        )

        s3_client = boto3.client("s3")
        s3_client.download_file(
            S3_BUCKET,
            S3_MODEL_KEY,
            LOCAL_MODEL_PATH
        )

        logger.info("Model download completed")

        with open(LOCAL_MODEL_PATH, "rb") as f:
            model = pickle.load(f)

        logger.info("Model loaded successfully into memory")
        return model

    except Exception as e:
        logger.error("Failed to load model", exc_info=True)
        raise CustomException(e, sys)


# Load model once at startup
model = load_model()


# -------------------- Routes --------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No input data provided"}), 400

        logger.info(f"Received prediction request: {data}")

        features = list(data.values())
        prediction = model.predict([features])

        logger.info(f"Prediction result: {prediction[0]}")

        return jsonify(
            {
                "prediction": float(prediction[0])
            }
        ), 200

    except Exception as e:
        logger.error("Prediction failed", exc_info=True)
        raise CustomException(e, sys)


# -------------------- App Runner --------------------
if __name__ == "__main__":
    logger.info("Starting Flask inference service on port 8080")
    app.run(host="0.0.0.0", port=8080)
