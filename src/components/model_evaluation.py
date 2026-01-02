import os
import sys
import json
import pickle
import boto3
import pandas as pd

from sklearn.metrics import r2_score

from src.logger.logger import logger
from src.exception.exception import CustomException


class ModelEvaluation:
    def __init__(self, metrics_cfg: dict, data_cfg: dict, s3_cfg: dict):
        self.metrics_cfg = metrics_cfg
        self.data_cfg = data_cfg
        self.s3_cfg = s3_cfg

        self.s3_client = boto3.client("s3")

        os.makedirs(self.metrics_cfg["metrics_dir"], exist_ok=True)
        logger.info(
            f"ModelEvaluation initialized with metrics_dir="
            f"{self.metrics_cfg['metrics_dir']}"
        )

    def evaluate(self, new_model_path: str, test_path: str) -> dict:
        try:
            logger.info("Starting model evaluation step")

            logger.info(f"Loading test data from {test_path}")
            df = pd.read_csv(test_path)

            X = pd.get_dummies(
                df.drop(self.data_cfg["target"], axis=1)
            )
            y = df[self.data_cfg["target"]]

            # -------------------- New Model Evaluation --------------------
            logger.info(f"Loading new model from {new_model_path}")
            with open(new_model_path, "rb") as f:
                new_model = pickle.load(f)

            new_predictions = new_model.predict(X)
            new_score = r2_score(y, new_predictions)

            logger.info(f"New model R2 score: {new_score}")

            # -------------------- Old Model Evaluation --------------------
            old_score = None
            old_model_path = "old_model.pkl"

            try:
                logger.info(
                    "Attempting to download existing production model from S3"
                )
                self.s3_client.download_file(
                    self.s3_cfg["bucket"],
                    self.s3_cfg["model_key"],
                    old_model_path
                )

                with open(old_model_path, "rb") as f:
                    old_model = pickle.load(f)

                old_predictions = old_model.predict(X)
                old_score = r2_score(y, old_predictions)

                logger.info(f"Old model R2 score: {old_score}")

            except Exception:
                logger.warning(
                    "No existing production model found in S3. "
                    "Assuming first deployment."
                )

            # -------------------- Promotion Decision --------------------
            promote = (
                old_score is None or new_score > old_score
            )

            metrics = {
                "new_model_r2": new_score,
                "old_model_r2": old_score,
                "promote": promote
            }

            metrics_path = os.path.join(
                self.metrics_cfg["metrics_dir"],
                "model_evaluation.json"
            )

            with open(metrics_path, "w") as f:
                json.dump(metrics, f, indent=4)

            logger.info(
                f"Model evaluation completed. Metrics saved at {metrics_path}"
            )
            logger.info(f"Promotion decision: {promote}")

            return metrics

        except Exception as e:
            logger.error("Failure occurred during model evaluation", exc_info=True)
            raise CustomException(e, sys)
