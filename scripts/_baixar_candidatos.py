"""Baixa (do bucket publico do Open Images) uma amostra de candidatos e reduz para no maximo 1024 px."""
import sys, io, pandas as pd, requests
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
meta, dest, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
import os; os.makedirs(dest, exist_ok=True)
cand = pd.read_csv(f"{meta}/candidatos.csv")
# amostra reprodutivel; vacas ordenadas pelo tamanho do maior animal (prioriza fotos "de perto")
vac = cand[cand.classe == "vaca"].sample(frac=1, random_state=6).head(n)
tra = cand[cand.classe == "trator"].sample(frac=1, random_state=6).head(n)
def get(row):
    split = "validation" if row.Subset == "validation" else "test"
    p = f"{dest}/{row.classe}_{row.ImageID}.jpg"
    if os.path.exists(p): return p
    r = requests.get(f"https://s3.amazonaws.com/open-images-dataset/{split}/{row.ImageID}.jpg", timeout=60)
    r.raise_for_status()
    im = Image.open(io.BytesIO(r.content)).convert("RGB")
    im.thumbnail((1024, 1024))
    im.save(p, quality=90)
    return p
rows = [r for _, r in pd.concat([vac, tra]).iterrows()]
with ThreadPoolExecutor(8) as ex:
    for res in ex.map(lambda r: (lambda: get(r))() , rows): pass
print("ok", len(os.listdir(dest)))
