import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

from src.logger.logger import logger
from src.exception.exception import CustomException


class DataTransformation:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        os.makedirs(self.cfg["processed_dir"], exist_ok=True)
        logger.info(
            f"DataTransformation initialized with processed_dir={self.cfg['processed_dir']}"
        )

    def split(self, raw_path: str):
        try:
            logger.info(f"Starting train-test split using raw data at {raw_path}")

            df = pd.read_csv(raw_path)
            logger.info(f"Raw dataset loaded with shape {df.shape}")

            train, test = train_test_split(
                df,
                test_size=self.cfg["test_size"],
                random_state=42
            )

            train_path = os.path.join(self.cfg["processed_dir"], "train.csv")
            test_path = os.path.join(self.cfg["processed_dir"], "test.csv")

            train.to_csv(train_path, index=False)
            test.to_csv(test_path, index=False)

            logger.info(
                f"Train-test split completed successfully. "
                f"Train shape: {train.shape}, Test shape: {test.shape}"
            )
            logger.info(
                f"Train data saved at {train_path}, Test data saved at {test_path}"
            )

            return train_path, test_path

        except Exception as e:
            logger.error("Failure occurred during data transformation", exc_info=True)
            raise CustomException(e, sys)
