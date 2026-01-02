import os
import sys
import pandas as pd

from src.logger.logger import logger
from src.exception.exception import CustomException


class DataIngestion:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        os.makedirs(self.cfg["raw_dir"], exist_ok=True)
        logger.info(f"DataIngestion initialized with raw_dir={self.cfg['raw_dir']}")

    def ingest(self) -> str:
        try:
            logger.info("Starting data ingestion process")

            logger.info(f"Reading data from URL: {self.cfg['url']}")
            df = pd.read_csv(self.cfg["url"])

            output_path = os.path.join(self.cfg["raw_dir"], "housing.csv")
            df.to_csv(output_path, index=False)

            logger.info(
                f"Raw data successfully saved at {output_path} "
                f"with shape {df.shape}"
            )

            return output_path

        except Exception as e:
            logger.error("Failure occurred during data ingestion", exc_info=True)
            raise CustomException(e, sys)
