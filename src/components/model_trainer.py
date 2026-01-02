import os
import sys
import pickle
import pandas as pd
import mlflow

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score

from src.logger.logger import logger
from src.exception.exception import CustomException


class ModelTrainer:
    def __init__(self, model_cfg: dict, data_cfg: dict, mlflow_cfg: dict):
        self.model_cfg = model_cfg
        self.data_cfg = data_cfg
        self.mlflow_cfg = mlflow_cfg

        os.makedirs(self.model_cfg["model_dir"], exist_ok=True)
        logger.info("ModelTrainer initialized")

        # Supported model registry
        self.model_registry = {
            "LinearRegression": LinearRegression,
            "RandomForest": RandomForestRegressor,
            "GradientBoosting": GradientBoostingRegressor
        }

    def train(self, train_path: str) -> str:
        try:
            logger.info("Starting hyperparameter-driven model training")

            mlflow.set_tracking_uri(self.mlflow_cfg["tracking_uri"])
            mlflow.set_experiment(self.mlflow_cfg["experiment_name"])

            df = pd.read_csv(train_path)

            X = pd.get_dummies(
                df.drop(self.data_cfg["target"], axis=1)
            )
            y = df[self.data_cfg["target"]]

            best_model = None
            best_score = float("-inf")
            best_model_name = None

            for model_name, params in self.model_cfg["candidates"].items():
                if model_name not in self.model_registry:
                    raise ValueError(f"Unsupported model: {model_name}")

                logger.info(
                    f"Training model: {model_name} with params: {params}"
                )

                model_class = self.model_registry[model_name]
                model = model_class(**params)

                with mlflow.start_run(run_name=model_name):
                    model.fit(X, y)
                    predictions = model.predict(X)
                    score = r2_score(y, predictions)

                    mlflow.log_metric("train_r2", score)
                    mlflow.log_metric("train_rows", len(X))

                    for param_key, param_value in params.items():
                        mlflow.log_param(param_key, param_value)

                    mlflow.log_param("model_name", model_name)
                    mlflow.sklearn.log_model(model, "model")

                    logger.info(
                        f"{model_name} completed with R2 score: {score}"
                    )

                    if score > best_score:
                        best_score = score
                        best_model = model
                        best_model_name = model_name

            logger.info(
                f"Best model selected: {best_model_name} "
                f"with R2 score: {best_score}"
            )

            model_path = os.path.join(
                self.model_cfg["model_dir"],
                self.model_cfg["model_name"]
            )

            with open(model_path, "wb") as f:
                pickle.dump(best_model, f)

            logger.info(
                f"Best model ({best_model_name}) saved at {model_path}"
            )

            return model_path

        except Exception as e:
            logger.error("Failure occurred during model training", exc_info=True)
            raise CustomException(e, sys)
