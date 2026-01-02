import os
import sys
import boto3

from src.logger.logger import logger
from src.exception.exception import CustomException


class ModelPusher:
    def __init__(self, cfg: dict):
        try:
            self.cfg = cfg
            self.s3_client = boto3.client("s3")

            logger.info(
                f"ModelPusher initialized with bucket={self.cfg['bucket']}, "
                f"model_key={self.cfg['model_key']}"
            )

        except Exception as e:
            logger.error(
                "Failed to initialize ModelPusher",
                exc_info=True
            )
            raise CustomException(e, sys)

    def push(self, model_path: str) -> None:
        try:
            logger.info(f"Starting model push to S3 from path: {model_path}")

            if not os.path.exists(model_path):
                raise FileNotFoundError(
                    f"Model file not found at path: {model_path}"
                )

            self.s3_client.upload_file(
                Filename=model_path,
                Bucket=self.cfg["bucket"],
                Key=self.cfg["model_key"]
            )

            logger.info(
                f"Model successfully uploaded to s3://{self.cfg['bucket']}/"
                f"{self.cfg['model_key']}"
            )

        except Exception as e:
            logger.error(
                "Failure occurred during model push to S3",
                exc_info=True
            )
            raise CustomException(e, sys)
