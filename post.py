import asyncio
import os
import random
import requests
from dataclasses import dataclass
from tqdm import tqdm
from pathlib import Path
from hydrogram import Client
from hydrogram.raw import functions, types
from hydrogram.errors.exceptions.unauthorized_401 import AuthKeyUnregistered
from config import load, save, ask

SESSION_NAME = "my_account"
PROXY_SETTINGS = {
    "scheme": "socks5",
    "hostname": "127.0.0.1",
    "port": 10801
}

INT64_MIN = -9223372036854775808
INT64_MAX = 9223372036854775807


@dataclass
class ProxyConfig:
    scheme: str
    hostname: str
    port: int

    @property
    def url(self) -> str:
        scheme_suffix = "h" if self.scheme == "socks5" else ""
        return f"{self.scheme}{scheme_suffix}://{self.hostname}:{self.port}"

    def is_working(self, timeout: int = 5) -> bool:
        proxies = {"http": self.url, "https": self.url}
        try:
            response = requests.get("https://1.1.1.1", proxies=proxies, timeout=timeout)
            return response.status_code == 200
        except requests.RequestException:
            return False

def load_valid_conf() -> tuple[int, str, int]:
    if not Path("part").exists():
        print("Папка отсутствует")
        exit(1)
    try:
        api_id, api_hash, count = load()
        for i in range(count):
            if not Path(f"part/{i}.jpg").exists():
                raise FileExistsError(f"Файл part/{i}.jpg не найден")
        return api_id, api_hash, count
    except FileExistsError:
        print("Сначала запустите prepare.py")
        exit(1)
    except KeyboardInterrupt as err:
        print(err)
        exit(1)

async def main():
    api_id, api_hash, count = load_valid_conf()
    if not ProxyConfig(**PROXY_SETTINGS).is_working():
        print("Запустите прокси")
        exit(1)

    app = Client(
        SESSION_NAME,
        api_id=api_id,
        api_hash=api_hash,
        proxy=PROXY_SETTINGS
    ) 

    try:
        async with app:
            print(f"Вы вошли как {await app.get_me()}")
            
            media = []
            print("Загрузка медиафайла...")
            for i in tqdm(range(count-1,-1,-1)):
                file = f'part/{i}.jpg'
                uploaded_file = await app.save_file(file)
                media.append(types.InputMediaUploadedPhoto(file=uploaded_file))

            print("Публикация сторисов...")
            peer = await app.resolve_peer("me")
            for i in tqdm(media):
                await app.invoke(
                    functions.stories.SendStory(
                        peer=peer,
                        media=i,
                        privacy_rules=[types.InputPrivacyValueAllowAll()],
                        random_id=random.randint(INT64_MIN, INT64_MAX)
                    )
                )
            print("Готово!")
            if ask("Выйти?"):
                await app.log_out()
                if Path("my_account.session").exists():
                    Path("my_account.session").unlink()
                print("Выход совершён")
    
    except AuthKeyUnregistered:
        print("Устаревшая / завершённая сессия")
        if Path("my_account.session").exists():
            Path("my_account.session").unlink()
    except EOFError:
        print("\nВыход")

if __name__ == "__main__":
    asyncio.run(main())
