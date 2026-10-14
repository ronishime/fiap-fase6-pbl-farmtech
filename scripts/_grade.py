"""Desenha grade de 10% (rotulada) sobre imagens para leitura manual de coordenadas normalizadas; 4 imagens por folha."""
import sys, glob, os
from PIL import Image, ImageDraw
src, out, ids = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
os.makedirs(out, exist_ok=True)
W = 700
for s in range(0, len(ids), 4):
    sheet = Image.new("RGB", (2 * W, 2 * W), "white"); d = ImageDraw.Draw(sheet)
    for k, p in enumerate(ids[s:s + 4]):
        f = glob.glob(f"{src}/trator_{p}*.jpg")[0]
        im = Image.open(f); im.thumbnail((W - 30, W - 30)); w, h = im.size
        x0, y0 = (k % 2) * W + 25, (k // 2) * W + 25
        sheet.paste(im, (x0, y0))
        for i in range(11):
            c = (255, 255, 0) if i % 5 else (255, 0, 255)
            d.line([x0 + i * w / 10, y0, x0 + i * w / 10, y0 + h], fill=c, width=1)
            d.line([x0, y0 + i * h / 10, x0 + w, y0 + i * h / 10], fill=c, width=1)
            d.text((x0 + i * w / 10 - 6, y0 - 12), str(i), fill="black")
            d.text((x0 - 14, y0 + i * h / 10 - 5), str(i), fill="black")
        d.text((x0, y0 + h + 2), p, fill="blue")
    sheet.save(f"{out}/grade_{s // 4}.jpg", quality=90)
print("ok")
