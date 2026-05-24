from __future__ import annotations
from pathlib import Path
from typing import Any, cast
import yaml

CONFIG_FILE = Path("config.yaml")

def ask(text: str) -> bool:
    while True:
        try:
            selection = input(f"{text.rstrip()} [Y/n]:").strip().lower()
            if selection in ("y", ""):
                return True
            if selection == "n":
                return False
            print("Please enter 'y' or 'n'.")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user.")
            return False
        
def read_config_file(file_path: Path) -> dict[str, Any]:
    try:
        with open(file_path, "r", encoding="utf-8") as file_stream:
            config_data = yaml.safe_load(file_stream)
            return cast(dict[str, Any], config_data) if isinstance(config_data, dict) else {}
    except (yaml.YAMLError, OSError):
        return {}

def save_config_file(file_path: Path, config_data: dict[str, Any]) -> bool:
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file_stream:
            yaml.safe_dump(config_data, file_stream, allow_unicode=True, sort_keys=False)
        return True
    except OSError:
        print(f"Error: Unable to write to config file at {file_path}")
        return False
        
def read(text: str, type: type = int) -> str | int | float | None:
    while True:
        try:
            return type(input(f"{text.rstrip()}: ").strip())
        except ValueError:
            print(f"Please enter a valid {type.__name__}.")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user.")
            return None

def load() -> tuple[int, str, int]:
    if CONFIG_FILE.exists():
        config = read_config_file(CONFIG_FILE)
        if "count" in config:
            if not ("api_id" in config and "api_hash" in config):
                print("Введите значения из my.telegram.org")
                config["api_id"] = read("Api id", int)
                if config["api_id"] is None:
                    raise KeyboardInterrupt("Настройка прервана пользователем.")
                config["api_hash"] = read("Api hash", str)
                if config["api_hash"] is None:
                    raise KeyboardInterrupt("Настройка прервана пользователем.")
                save_config_file(CONFIG_FILE, config)
            return (int(config["api_id"]), str(config["api_hash"]), int(config["count"]))
    raise FileExistsError("Сначала запустите prepare.py")

def save(count: int, api_id: int | None = None, api_hash: str | None = None, reset: bool = False) -> None:
    if reset:
        config = {}
    else:
        config = read_config_file(CONFIG_FILE)
    config["count"] = count
    if api_id and api_hash:
        config["api_id"] = api_id
        config["api_hash"] = api_hash      
    save_config_file(CONFIG_FILE, config)
