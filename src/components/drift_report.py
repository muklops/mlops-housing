import os
import sys
import pandas as pd

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

from src.logger.logger import logger
from src.exception.exception import CustomException


class DriftReport:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        os.makedirs(self.cfg["reports_dir"], exist_ok=True)
        logger.info("DriftReport initialized")

    def generate(self, train_path: str, test_path: str) -> None:
        try:
            logger.info("Starting Evidently data drift analysis")

            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logger.info(
                f"Reference data shape: {train_df.shape}, "
                f"Current data shape: {test_df.shape}"
            )

            report = Report(
                metrics=[
                    DataDriftPreset()
                ]
            )

            report.run(
                reference_data=train_df,
                current_data=test_df
            )

            report_path = os.path.join(
                self.cfg["reports_dir"],
                "data_drift_report.html"
            )

            report.save_html(report_path)

            logger.info(
                f"Evidently data drift report generated at {report_path}"
            )

        except Exception as e:
            logger.error(
                "Failure occurred during data drift analysis",
                exc_info=True
            )
            raise CustomException(e, sys)
