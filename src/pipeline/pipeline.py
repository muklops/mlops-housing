import sys
import yaml

from src.logger.logger import logger
from src.exception.exception import CustomException

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.drift_report import DriftReport
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher


def run_pipeline() -> None:
    try:
        logger.info("=" * 70)
        logger.info("Starting end-to-end ML pipeline")
        logger.info("=" * 70)

        # -------------------- Load Config --------------------
        logger.info("Loading configuration from config/config.yaml")
        with open("config/config.yaml", "r") as f:
            cfg = yaml.safe_load(f)

        # -------------------- Data Ingestion --------------------
        logger.info("Stage: Data Ingestion")
        raw_data_path = DataIngestion(cfg["data"]).ingest()

        # -------------------- Data Validation -------------------
        logger.info("Stage: Data Validation")
        DataValidation(cfg["data"]).validate(raw_data_path)

        # -------------------- Data Transformation ---------------
        logger.info("Stage: Data Transformation")
        train_path, test_path = DataTransformation(cfg["data"]).split(raw_data_path)

        # -------------------- Model Training --------------------
        logger.info("Stage: Model Training")
        model_path = ModelTrainer(
            model_cfg=cfg["model"],
            data_cfg=cfg["data"],
            mlflow_cfg=cfg["mlflow"]
        ).train(train_path)

        # -------------------- Evidently Drift Report -------------
        logger.info("Stage: Data Drift Analysis (Evidently)")
        DriftReport(cfg["metrics"]).generate(
            train_path=train_path,
            test_path=test_path
        )

        # -------------------- Model Evaluation ------------------
        logger.info("Stage: Model Evaluation")
        metrics = ModelEvaluation(
            metrics_cfg=cfg["metrics"],
            data_cfg=cfg["data"],
            s3_cfg=cfg["s3"]
        ).evaluate(
            new_model_path=model_path,
            test_path=test_path
        )

        # -------------------- Model Promotion -------------------
        if metrics.get("promote", False):
            logger.info("New model approved for promotion")
            ModelPusher(cfg["s3"]).push(model_path)
        else:
            logger.info("New model rejected. Production model retained")

        logger.info("=" * 70)
        logger.info("Pipeline completed successfully")
        logger.info("=" * 70)

    except Exception as e:
        logger.error("Pipeline execution failed", exc_info=True)
        raise CustomException(e, sys)
