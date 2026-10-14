"""Pre-rotulos dos tratores com o detector open-vocabulary YOLO-World (o Open Images nao tem caixas de 'Tractor').
Saida: CSV no mesmo formato das caixas do Open Images (coordenadas normalizadas) para revisao no Make Sense."""
import sys, glob, os, pandas as pd
from ultralytics import YOLOWorld
sys.path.insert(0, os.path.dirname(__file__))
from _selecao import TRATOR
src, out_csv = sys.argv[1], sys.argv[2]
model = YOLOWorld("yolov8l-worldv2.pt")
CLASSES = ["tractor", "trailer", "combine harvester", "hay baler", "plow", "seeder", "tank", "person"]
model.set_classes(CLASSES)
rows = []
for p in TRATOR:
    f = glob.glob(f"{src}/trator_{p}*.jpg")[0]
    r = model.predict(f, conf=0.25, iou=0.5, verbose=False)[0]
    if not (r.boxes.cls == 0).any():  # sem caixa confiante: fica com a melhor caixa de baixa confianca (revisar no Make Sense)
        r = model.predict(f, conf=0.01, iou=0.5, classes=[0], max_det=1, verbose=False)[0]
    for (x1, y1, x2, y2), c, k in zip(r.boxes.xyxyn.tolist(), r.boxes.conf.tolist(), r.boxes.cls.tolist()):
        if k != 0: continue  # so a classe trator vira rotulo
        rows.append(dict(ImageID=os.path.basename(f)[7:-4], XMin=x1, XMax=x2, YMin=y1, YMax=y2, conf=c))
df = pd.DataFrame(rows)
df.to_csv(out_csv, index=False)
print(df.groupby("ImageID").size().value_counts().sort_index(), "\nsem caixa:",
      [p for p in TRATOR if not df.ImageID.str.startswith(p).any()])
