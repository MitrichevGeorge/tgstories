from __future__ import annotations
from PIL import Image, UnidentifiedImageError
from math import ceil
from pathlib import Path
from config import save, ask
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.formatted_text import HTML
from tqdm import tqdm
from shutil import rmtree

EACH_WIDTH = 1360
EACH_HEIGHT = 1704
MARGIN = 16
ALL_WIDTH = EACH_WIDTH * 3 + MARGIN * 2

SAVE_PATH = Path("part")

def get_file_name() -> str | None:
    try:
        file_completer = PathCompleter(only_directories=False, expanduser=True)
        user_input = prompt(
            HTML('Введите путь к картинке: '),
            completer=file_completer,
            complete_while_typing=True
        )
        if not user_input:
            print("Путь к файлу не может быть пустым.")
            return None
        if not Path(user_input).is_file():
            print("Указанный путь не является файлом.")
            return None
        return user_input
    except (KeyboardInterrupt, EOFError):
        print("\nОперация отменена пользователем.")
        return None
    
def resize_image(image: Image.Image) -> Image.Image:
    width, height = image.size
    print(f"Initial: {width}, {height}")
    height = round((height/width)*ALL_WIDTH)
    image = image.resize((ALL_WIDTH, height))
    print(f"Now: {image.size}")
    return image

def readable_size(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            if unit == 'B':
                return f"{size} {unit}"
            return f"{size:.2f} {unit}"
        size = int(size / 1024.0)
    return f"{size:.2f} PB"

file_path = get_file_name()
if not file_path:
    exit(1)

try:
    img: Image.Image = Image.open(file_path)
except UnidentifiedImageError:
    print("Файл не является допустимым изображением.")
    exit(1)
except (OSError, IOError) as e:
    print(f"Ошибка при открытии изображения: {e}")
    exit(1)

img = resize_image(img)

if not SAVE_PATH.exists():
    try:
        SAVE_PATH.mkdir(parents=True)
    except OSError as e:
        print(f"Ошибка при создании папки для сохранения: {e}")
        exit(1)
else:
    if not SAVE_PATH.is_dir():
        print(f"Путь {SAVE_PATH} существует и не является директорией.")
        exit(1)
    if any(SAVE_PATH.iterdir()):
        if ask(f"Папка {SAVE_PATH} не пуста. Очистить её?"):
            try:
                for file in SAVE_PATH.iterdir():
                    if file.is_dir():
                        rmtree(file)
                    else:
                        file.unlink()
                print(f"Папка {SAVE_PATH} очищена.")
            except OSError as e:
                print(f"Ошибка при очистке папки: {e}")
                exit(1)

vertical_count = ceil(img.size[1] / EACH_HEIGHT)
if img.size[1] % EACH_HEIGHT < EACH_HEIGHT // 3:
    if ask(f"Последняя часть будет {img.size[1] % EACH_HEIGHT / EACH_HEIGHT * 100:.2f}% от обычной. Убрать её?"):
        vertical_count -= 1
total_images = vertical_count * 3
count, total_bytes = 0, 0

with tqdm(total=total_images) as pbar:
    for y in range(vertical_count):
        for x in range(3):
            path = SAVE_PATH / f"{count}.jpg"
            left = (EACH_WIDTH + MARGIN) * x
            top = (EACH_HEIGHT + MARGIN) * y
            q = img.crop((left, top, left + EACH_WIDTH, EACH_HEIGHT + top))
            q.save(path)
            total_bytes += path.stat().st_size
            count += 1
            pbar.update(1)

save(count)
print(f"Всего частей: {count}, общий размер: {readable_size(total_bytes)}")
