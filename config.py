from pathlib import Path
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

def get_config_vars():
    # Если файла нет — создаем его (используем логику из прошлого шага)
    # ... (код создания файла) ...

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    # Возвращаем кортеж значений в строгом порядке
    return config.get("api_key"), config.get("username")


# Вот ваш красивый импорт в одну строку:
KEY, NAME = get_config_vars()

print(f"Ключ: {KEY}, Имя: {NAME}")

CONFIG_FILE = Path("config.yaml")

def load(is_second: bool = True) -> tuple:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
            if not all("api_id" in config,"api_hash" in config):
                raise ValueError("Не всё есть в конфиге")
            return (config.get("api_id"), config.get("api_hash"), config.get("count"))
    if is_second:
        raise FileExistsError("Сначала запустите prepare.py")
    print("Введите из my.telegram.org")

    config = {
        "api_id": input("Api key: ").strip(),
        "api_hash": input("Api hash: ").strip(),
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f, allow_unicode=True, sort_keys=False)

    return (config.get("api_id"), config.get("api_hash"), config.get("count"))

def save(api_id: int, api_hash: str, )


if __name__ == "__main__":
    user_config = load_or_create_config()
    print(f"Данные в коде: {user_config}")