import asyncio
import os
import random
from hydrogram import Client
from hydrogram.raw import functions, types

API_ID = 24562157
API_HASH = "6ec6241e31f57d6cbe7e82e6258b2668"
N = 15

proxy_settings = {
    "scheme": "socks5",
    "hostname": "127.0.0.1",
    "port": 10801
}

async def main():
    app = Client(
        "my_account",
        api_id=API_ID,
        api_hash=API_HASH,
        proxy=proxy_settings
    )

    async with app:
        print("Сессия активна!")
        
        media = []
        print("Загрузка медиафайла...")
        for i in range(N-1,-1,-1):
            file = f'part/{i}.jpg'
            print(file, end="...")
            uploaded_file = await app.save_file(file)
            media.append(types.InputMediaUploadedPhoto(file=uploaded_file))
            print("OK")
    
        for i in media:
            print("Отправка истории...")
            result = await app.invoke(
                functions.stories.SendStory(
                    peer=await app.resolve_peer("me"),
                    media=i,
                    privacy_rules=[types.InputPrivacyValueAllowAll()],
                    random_id=random.randint(-9223372036854775808, 9223372036854775807)
                )
            )
        print("Готово! История успешно опубликована.")

if __name__ == "__main__":
    asyncio.run(main())
