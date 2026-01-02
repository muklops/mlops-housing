import os
import sys
import json
import pandas as pd

from src.logger.logger import logger
from src.exception.exception import CustomException


class DataValidation:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.validation_dir = os.path.join("artifacts", "metrics")
        os.makedirs(self.validation_dir, exist_ok=True)

        logger.info("DataValidation initialized")

    def validate(self, raw_data_path: str) -> bool:
        try:
            logger.info(f"Starting data validation for file: {raw_data_path}")

            df = pd.read_csv(raw_data_path)
            logger.info(f"Dataset loaded with shape {df.shape}")

            validation_report = {
                "file_path": raw_data_path,
                "row_count": df.shape[0],
                "column_count": df.shape[1],
                "missing_values": {},
                "duplicate_rows": 0,
                "target_column_present": False,
                "status": "FAILED"
            }

            # 1. Check missing values
            missing_counts = df.isnull().sum()
            missing_columns = missing_counts[missing_counts > 0]

            validation_report["missing_values"] = missing_columns.to_dict()

            if missing_columns.any():
                logger.warning(
                    f"Missing values found in columns: {missing_columns.to_dict()}"
                )
            else:
                logger.info("No missing values found")

            # 2. Check duplicate rows
            duplicate_count = df.duplicated().sum()
            validation_report["duplicate_rows"] = int(duplicate_count)

            if duplicate_count > 0:
                logger.warning(f"Duplicate rows detected: {duplicate_count}")
            else:
                logger.info("No duplicate rows found")

            # 3. Check target column existence
            target_col = self.cfg["target"]
            if target_col in df.columns:
                validation_report["target_column_present"] = True
                logger.info(f"Target column '{target_col}' is present")
            else:
                logger.error(f"Target column '{target_col}' is missing")
                raise ValueError(f"Target column '{target_col}' not found")

            # Final status
            validation_report["status"] = "PASSED"

            report_path = os.path.join(
                self.validation_dir, "data_validation_report.json"
            )
            with open(report_path, "w") as f:
                json.dump(validation_report, f, indent=4)

            logger.info(
                f"Data validation completed successfully. "
                f"Report saved at {report_path}"
            )

            return True

        except Exception as e:
            logger.error("Data validation failed", exc_info=True)
            raise CustomException(e, sys)
