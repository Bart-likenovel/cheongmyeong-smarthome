"""AI 원본 PNG를 사이트용으로 최적화한다.
- 사진: 1600px JPG(q82) 생성, 원본 PNG는 ../ai_originals/ 로 이동(사이트 배포물에서 제외)
- 로고: 투명 여백을 잘라 256px PNG로 저장(원본은 ai_originals에 보관)
사용: python3 -I tools/optimize-images.py
"""
import os, shutil, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AI = os.path.join(ROOT, "assets", "img", "ai")
ORIG = os.path.join(os.path.dirname(ROOT), "ai_originals")
os.makedirs(ORIG, exist_ok=True)

for f in sorted(os.listdir(AI)):
    if not f.endswith(".png"):
        continue
    src = os.path.join(AI, f)
    im = Image.open(src)
    if f == "logo-mark.png":
        if im.size == (256, 256):
            continue  # 이미 최적화됨. 다시 처리하면 보관 원본을 축소본으로 덮어쓴다
        shutil.copy2(src, os.path.join(ORIG, f))
        bbox = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
        im = im.crop(bbox)
        side = max(im.size) + 24
        canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        canvas.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
        canvas.resize((256, 256), Image.LANCZOS).save(src, optimize=True)
        print("logo", os.path.getsize(src))
        continue
    im = im.convert("RGB")
    if im.width > 1600:
        im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
    dst = os.path.join(AI, f[:-4] + ".jpg")
    im.save(dst, quality=82, optimize=True, progressive=True)
    shutil.move(src, os.path.join(ORIG, f))
    print(f, "->", os.path.basename(dst), os.path.getsize(dst))
