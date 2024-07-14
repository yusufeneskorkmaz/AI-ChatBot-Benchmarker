import os
import yaml
import json
from box import ConfigBox
from pathlib import Path

def read_yaml(path_to_yaml: str) -> ConfigBox:
    """reads yaml file and returns ConfigBox"""
    with open(path_to_yaml) as yaml_file:
        content = yaml.safe_load(yaml_file)
    return ConfigBox(content)

def create_directories(path_to_directories: list, verbose=True):
    """create list of directories"""
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            print(f"created directory at: {path}")

def save_json(path: str, data: dict):
    """save json data"""
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_json(path: str) -> ConfigBox:
    """load json files data"""
    with open(path) as f:
        content = json.load(f)
    return ConfigBox(content)

def get_size(path: str):
    """get size in KB"""
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"