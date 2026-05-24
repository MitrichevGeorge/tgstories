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

API_ID = 0
API_HASH = ""
COUNT = 0
SESSION = "my_account"

proxy_settings = {
    "scheme": "socks5",
    "hostname": "127.0.0.1",
    "port": 10801
}


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

def prepare():
    if not Path("part").exists():
        print("Папка отсутствует")
        exit(1)
    try:
        API_ID, API_HASH, COUNT = load()
        for i in range(COUNT):
            if not Path(f"part/{i}.jpg").exists():
                raise FileExistsError()
        return API_ID, API_HASH, COUNT
    except FileExistsError:
        print("Сначала запустите prepare.py")
        exit(1)
    except KeyboardInterrupt as err:
        print(err)
        exit(1)

async def main():
    API_ID, API_HASH, COUNT = prepare()
    if not ProxyConfig(**proxy_settings).is_working():
        print("Запустите прокси")
        exit(1)
    app = Client(
        SESSION,
        api_id=API_ID,
        api_hash=API_HASH,
        proxy=proxy_settings
    ) 

    try:
        async with app:
            print(f"Вы вошли как {await app.get_me()}")
            
            media = []
            print("Загрузка медиафайла...")
            for i in tqdm(range(COUNT-1,-1,-1)):
                file = f'part/{i}.jpg'
                uploaded_file = await app.save_file(file)
                media.append(types.InputMediaUploadedPhoto(file=uploaded_file))
        
            for i in tqdm(media):
                result = await app.invoke(
                    functions.stories.SendStory(
                        peer=await app.resolve_peer("me"),
                        media=i,
                        privacy_rules=[types.InputPrivacyValueAllowAll()],
                        random_id=random.randint(-9223372036854775808, 9223372036854775807)
                    )
                )
            print("Готово! История успешно опубликована.")
            if ask("Выйти?"):
                await app.log_out()
                if Path("my_account.session").exists():
                    Path("my_account.session").unlink()
                print("Выход совершён")
    
    except AuthKeyUnregistered:
        print("Устаревшая / заверённая сессия")
        if Path("my_account.session").exists():
            Path("my_account.session").unlink()
    except EOFError:
        print("\nВыход")

if __name__ == "__main__":
    asyncio.run(main())
