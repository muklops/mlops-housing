import os

PROJECT_NAME = "mlops-housing"

# List of directories to create
DIRS = [
    f"{PROJECT_NAME}/.github/workflows",
    f"{PROJECT_NAME}/config",
    f"{PROJECT_NAME}/artifacts/raw",
    f"{PROJECT_NAME}/artifacts/processed",
    f"{PROJECT_NAME}/artifacts/model",
    f"{PROJECT_NAME}/artifacts/metrics",
    f"{PROJECT_NAME}/artifacts/reports",
    f"{PROJECT_NAME}/src/logger",
    f"{PROJECT_NAME}/src/exception",
    f"{PROJECT_NAME}/src/components",
    f"{PROJECT_NAME}/src/pipeline",
]

# List of files to create
FILES = [
    f"{PROJECT_NAME}/.github/workflows/ci.yml",
    f"{PROJECT_NAME}/.github/workflows/cd.yml",

    f"{PROJECT_NAME}/config/__init__.py",
    f"{PROJECT_NAME}/config/config.yaml",

    f"{PROJECT_NAME}/src/__init__.py",

    f"{PROJECT_NAME}/src/logger/__init__.py",
    f"{PROJECT_NAME}/src/logger/logger.py",

    f"{PROJECT_NAME}/src/exception/__init__.py",
    f"{PROJECT_NAME}/src/exception/exception.py",

    f"{PROJECT_NAME}/src/components/__init__.py",
    f"{PROJECT_NAME}/src/components/data_ingestion.py",
    f"{PROJECT_NAME}/src/components/data_transformation.py",
    f"{PROJECT_NAME}/src/components/model_trainer.py",
    f"{PROJECT_NAME}/src/components/model_evaluation.py",
    f"{PROJECT_NAME}/src/components/model_pusher.py",
    f"{PROJECT_NAME}/src/components/drift_report.py",

    f"{PROJECT_NAME}/src/pipeline/__init__.py",
    f"{PROJECT_NAME}/src/pipeline/pipeline.py",

    f"{PROJECT_NAME}/app.py",
    f"{PROJECT_NAME}/demo.py",
    f"{PROJECT_NAME}/dvc.yaml",
    f"{PROJECT_NAME}/Dockerfile",
    f"{PROJECT_NAME}/requirements.txt",
    f"{PROJECT_NAME}/setup.py",
    f"{PROJECT_NAME}/README.md",
]

def create_structure():
    # Create directories
    for dir_path in DIRS:
        os.makedirs(dir_path, exist_ok=True)

    # Create empty files
    for file_path in FILES:
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                pass

    print(" MLOps project structure created successfully!")

if __name__ == "__main__":
    create_structure()
