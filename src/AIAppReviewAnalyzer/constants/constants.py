from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.parent.parent

# Configuration files
CONFIG_FILE_PATH = ROOT_DIR / "config" / "config.yaml"
PARAMS_FILE_PATH = ROOT_DIR / "config" / "params.yaml"

# Data directories
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Model directory
MODEL_DIR = ROOT_DIR / "models"

# Logs directory
LOGS_DIR = ROOT_DIR / "logs"

# Results directory
RESULTS_DIR = ROOT_DIR / "results"