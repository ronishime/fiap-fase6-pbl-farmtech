"""Monta a base vaca x trator a partir das imagens do Open Images V7 escolhidas na curadoria.

Uso (nao precisa ser executado para rodar o notebook; a base ja esta pronta em dataset/):
    python scripts/montar_dataset.py <pasta_metadados_oi> <pasta_imagens_baixadas> <pasta_saida>

- 40 imagens por classe vao para a base principal (32 treino, 4 validacao, 4 teste), sorteadas com semente fixa;
- 20 imagens por classe vao para um teste extra (dataset_teste_extra), usado so para dar robustez a comparacao da Entrega 2;
- pre-rotulos no formato YOLO (classe xc yc w h normalizados): caixas humanas do Open Images (vaca)
  e caixas do YOLO-World revisadas manualmente (trator); a revisao final e feita no Make Sense.
"""
import sys, os, glob, shutil, random
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from _selecao import VACA, TRATOR
from _ajustes_manuais import AJUSTES_TRATOR

meta, imgs, out = sys.argv[1:4]
CLASSES = ["vaca", "trator"]
SPLITS = {"train": 32, "val": 4, "test": 4}

info = pd.read_csv(f"{meta}/candidatos.csv").set_index("ImageID")
cx_vaca = pd.read_csv(f"{meta}/caixas_vaca.csv")
cx_trat = pd.read_csv(f"{meta}/caixas_trator_yw2.csv")

def caixas(classe, iid):
    """Lista de caixas (xmin, ymin, xmax, ymax) normalizadas para a imagem."""
    if classe == "vaca":
        d = cx_vaca[cx_vaca.ImageID == iid]
    else:
        if iid[:8] in AJUSTES_TRATOR:
            return AJUSTES_TRATOR[iid[:8]]
        d = cx_trat[cx_trat.ImageID == iid]
    return list(d[["XMin", "YMin", "XMax", "YMax"]].itertuples(index=False, name=None))

rng = random.Random(2026)
creditos = []
for k, (classe, prefixos) in enumerate([("vaca", VACA), ("trator", TRATOR)]):
    ids = [os.path.basename(glob.glob(f"{imgs}/{classe}_{p}*.jpg")[0])[len(classe) + 1:-4] for p in prefixos]
    rng.shuffle(ids)
    principal, extra = ids[:40], ids[40:]
    destino = []
    i = 0
    for split, n in SPLITS.items():
        for iid in principal[i:i + n]:
            destino.append(("dataset", split, iid))
        i += n
    destino += [("dataset_teste_extra", "test", iid) for iid in extra]
    cont = {}
    for base, split, iid in destino:
        cont[base] = cont.get(base, 0) + 1
        nome = f"{classe}_{cont[base]:02d}" if base == "dataset" else f"{classe}_extra_{cont[base]:02d}"
        di, dl = f"{out}/{base}/images/{split}", f"{out}/{base}/labels/{split}"
        os.makedirs(di, exist_ok=True); os.makedirs(dl, exist_ok=True)
        shutil.copy(glob.glob(f"{imgs}/{classe}_{iid}.jpg")[0], f"{di}/{nome}.jpg")
        with open(f"{dl}/{nome}.txt", "w") as f:
            for x1, y1, x2, y2 in caixas(classe, iid):
                x1, y1, x2, y2 = [min(max(v, 0.0), 1.0) for v in (x1, y1, x2, y2)]
                f.write(f"{k} {(x1 + x2) / 2:.6f} {(y1 + y2) / 2:.6f} {x2 - x1:.6f} {y2 - y1:.6f}\n")
        r = info.loc[iid]
        creditos.append(dict(arquivo=f"{base}/images/{split}/{nome}.jpg", classe=classe, split=split,
                             open_images_id=iid, titulo=r.Title, autor=r.Author, licenca=r.License,
                             url_original=r.OriginalLandingURL))
pd.DataFrame(creditos).to_csv(f"{out}/creditos_imagens.csv", index=False)
for base in ("dataset", "dataset_teste_extra"):
    with open(f"{out}/{base}/classes.txt", "w") as f:
        f.write("\n".join(CLASSES) + "\n")
print(pd.DataFrame(creditos).groupby(["classe", "split"]).size())
