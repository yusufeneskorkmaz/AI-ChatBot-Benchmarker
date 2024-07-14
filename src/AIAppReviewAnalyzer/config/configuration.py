from src.AIAppReviewAnalyzer.utils.common import read_yaml, create_directories
from src.AIAppReviewAnalyzer.constants.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from pathlib import Path
import os

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self):
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )

        return data_ingestion_config

    def get_data_validation_config(self):
        config = self.config.data_validation
        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            ALL_REQUIRED_FILES=config.ALL_REQUIRED_FILES,
        )

        return data_validation_config

    def get_data_transformation_config(self):
        config = self.config.data_transformation
        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            tokenizer_name=config.tokenizer_name
        )

        return data_transformation_config

    def get_model_trainer_config(self):
        config = self.config.model_trainer
        params = self.params.TrainingArguments

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            model_ckpt=config.model_ckpt,
            num_train_epochs=params.num_train_epochs,
            warmup_steps=params.warmup_steps,
            per_device_train_batch_size=params.per_device_train_batch_size,
            weight_decay=params.weight_decay,
            logging_steps=params.logging_steps,
            evaluation_strategy=params.evaluation_strategy,
            eval_steps=params.evaluation_strategy,
            save_steps=params.save_steps,
            gradient_accumulation_steps=params.gradient_accumulation_steps
        )

        return model_trainer_config


class DataIngestionConfig:
    def __init__(self, root_dir, source_URL, local_data_file, unzip_dir):
        self.root_dir = root_dir
        self.source_URL = source_URL
        self.local_data_file = local_data_file
        self.unzip_dir = unzip_dir


class DataValidationConfig:
    def __init__(self, root_dir, STATUS_FILE, ALL_REQUIRED_FILES):
        self.root_dir = root_dir
        self.STATUS_FILE = STATUS_FILE
        self.ALL_REQUIRED_FILES = ALL_REQUIRED_FILES


class DataTransformationConfig:
    def __init__(self, root_dir, data_path, tokenizer_name):
        self.root_dir = root_dir
        self.data_path = data_path
        self.tokenizer_name = tokenizer_name


class ModelTrainerConfig:
    def __init__(self, root_dir, data_path, model_ckpt, num_train_epochs, warmup_steps,
                 per_device_train_batch_size, weight_decay, logging_steps, evaluation_strategy,
                 eval_steps, save_steps, gradient_accumulation_steps):
        self.root_dir = root_dir
        self.data_path = data_path
        self.model_ckpt = model_ckpt
        self.num_train_epochs = num_train_epochs
        self.warmup_steps = warmup_steps
        self.per_device_train_batch_size = per_device_train_batch_size
        self.weight_decay = weight_decay
        self.logging_steps = logging_steps
        self.evaluation_strategy = evaluation_strategy
        self.eval_steps = eval_steps
        self.save_steps = save_steps
        self.gradient_accumulation_steps = gradient_accumulation_steps