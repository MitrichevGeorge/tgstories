from PIL import Image
from math import ceil

img = Image.open("img/b.jpg")
# 1360x1704 + 16 -> 4112
w, h = img.size
print(f"initial: {w}, {h}")
h = round((h/w)*4112)
img = img.resize((4112, h))
print(f"now: {img.size}")
# img.show()
n = ceil(h / 1704)
k = 0
for y in range(n):
    for i in range(3):
        left = (1360 + 16) * i
        top = (1704 + 16) * y
        q = img.crop((left, top, left + 1360, 1704 + top))
        q.save(f"part/{k}.jpg")
        k += 1
