"""Folhas de contato a partir dos rotulos YOLO (confere a conversao)."""
import sys, glob, os
from PIL import Image, ImageDraw
base, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
files = sorted(glob.glob(f"{base}/images/*/*.jpg"))
T, C, R = 240, 6, 5
cor = {0: "red", 1: "cyan"}
for s in range(0, len(files), C * R):
    sheet = Image.new("RGB", (C * T, R * T), "white"); d = ImageDraw.Draw(sheet)
    for k, f in enumerate(files[s:s + C * R]):
        im = Image.open(f); im.thumbnail((T - 4, T - 18)); tw, th = im.size
        x0, y0 = (k % C) * T + 2, (k // C) * T + 16
        sheet.paste(im, (x0, y0))
        lab = f.replace("images", "labels")[:-4] + ".txt"
        for line in open(lab):
            c, xc, yc, w, h = line.split(); c = int(c); xc, yc, w, h = map(float, (xc, yc, w, h))
            d.rectangle([x0 + (xc - w / 2) * tw, y0 + (yc - h / 2) * th, x0 + (xc + w / 2) * tw, y0 + (yc + h / 2) * th], outline=cor[c], width=2)
        d.text((x0, y0 - 14), os.path.relpath(f, base).replace("images", "")[1:], fill="black")
    sheet.save(f"{out}/{os.path.basename(base)}_{s // (C * R)}.jpg", quality=85)
print("ok")
