import json
import os

CONFIG_FILE = "untold.json"

DEFAULT_CONFIG = {
    "name":         "my-project",
    "version":      "0.1.0",
    "description":  "",
    "author":       "",
    "license":      "MIT",
    "entry":        "main.ut",
    "dependencies": {},
    "scripts": {
        "start": "main.ut",
        "test":  "tests/test.ut"
    }
}

def load_config(path=None):
    cfg_path = path or os.path.join(os.getcwd(), CONFIG_FILE)
    if not os.path.exists(cfg_path):
        return None
    with open(cfg_path, "r") as f:
        return json.load(f)

def save_config(config, path=None):
    cfg_path = path or os.path.join(os.getcwd(), CONFIG_FILE)
    with open(cfg_path, "w") as f:
        json.dump(config, f, indent=2)
    return cfg_path

def init_config(name, author="", description=""):
    cfg = DEFAULT_CONFIG.copy()
    cfg["name"]        = name
    cfg["author"]      = author
    cfg["description"] = description
    return cfg

def find_project_root():
    """Walk up directory tree to find untold.json"""
    current = os.getcwd()
    while True:
        if os.path.exists(os.path.join(current, CONFIG_FILE)):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent