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

def load(is_second: bool = True) -> tuple[int, str, int | None]:
    if CONFIG_FILE.exists():
        config = read_config_file(CONFIG_FILE)
        if "api_id" in config and "api_hash" in config:
            return (config.get("api_id"), config.get("api_hash"), config.get("count"))
        print("Config file is missing required fields")
    if is_second:
        raise FileExistsError("Сначала запустите prepare.py")
    print("Введите из my.telegram.org")

    config = {
        "api_id": read("Api key: ", int),
        "api_hash": read("Api hash: ", str),
    }

    save_config_file(CONFIG_FILE, config)

    return (config.get("api_id"), config.get("api_hash"), None)

def save(api_id: int, api_hash: str, count: int | None = None) -> None:
    config = {
        "api_id": api_id,
        "api_hash": api_hash,
    }
    if count is not None:
        config["count"] = count

    save_config_file(CONFIG_FILE, config)
