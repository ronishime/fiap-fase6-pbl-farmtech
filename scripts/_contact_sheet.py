"""Gera folhas de contato numeradas (com caixas opcionais) para curadoria visual."""
import sys, os, glob, pandas as pd
from PIL import Image, ImageDraw
src, out, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
boxes = pd.read_csv(sys.argv[4]) if len(sys.argv) > 4 else None
files = sorted(glob.glob(f"{src}/{prefix}_*.jpg"))
os.makedirs(out, exist_ok=True)
T, C, R = 240, 6, 5
for s in range(0, len(files), C * R):
    sheet = Image.new("RGB", (C * T, R * T), "white")
    d = ImageDraw.Draw(sheet)
    for k, f in enumerate(files[s:s + C * R]):
        im = Image.open(f); w, h = im.size
        im.thumbnail((T - 4, T - 18)); tw, th = im.size
        x0, y0 = (k % C) * T + 2, (k // C) * T + 16
        sheet.paste(im, (x0, y0))
        iid = os.path.basename(f).split("_", 1)[1][:-4]
        if boxes is not None:
            for _, b in boxes[boxes.ImageID == iid].iterrows():
                d.rectangle([x0 + b.XMin * tw, y0 + b.YMin * th, x0 + b.XMax * tw, y0 + b.YMax * th], outline="red", width=2)
        d.text((x0, y0 - 14), f"{s + k}: {iid[:8]}", fill="black")
    sheet.save(f"{out}/{prefix}_{s // (C * R)}.jpg", quality=85)
print("ok")
