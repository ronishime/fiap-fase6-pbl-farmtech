"""Copia os rotulos exportados do Make Sense (formato YOLO) para as pastas da base.

Uso:
    python scripts/importar_rotulos_makesense.py rotulacao_makesense/<arquivo_exportado>.zip

O Make Sense exporta um .txt por imagem (mesmo nome da imagem) dentro de um .zip. Este script descobre,
pelo nome do arquivo, em qual pasta (train/val/test ou teste extra) esta a imagem correspondente e grava o
rotulo ao lado dela em labels/<split>/. Imagens sem rotulo exportado sao listadas como alerta.
"""
import sys, zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]                     # pasta do projeto
origem = Path(sys.argv[1])                                    # .zip exportado (ou pasta ja descompactada)
if origem.suffix == ".zip":                                   # le os .txt direto do zip
    with zipfile.ZipFile(origem) as z:
        rotulos = {Path(n).stem: z.read(n).decode() for n in z.namelist() if n.endswith(".txt")}
else:                                                         # ou de uma pasta com os .txt
    rotulos = {p.stem: p.read_text() for p in origem.glob("*.txt")}
rotulos.pop("labels", None)                                    # labels.txt e a lista de classes, nao um rotulo

imagens = sorted(RAIZ.glob("dataset*/images/*/*.jpg"))         # todas as imagens da base principal e do teste extra
faltando = []
for img in imagens:
    if img.stem not in rotulos:                               # imagem sem caixa exportada
        faltando.append(img.name)
        continue
    destino = img.parents[2] / "labels" / img.parent.name / f"{img.stem}.txt"   # dataset/labels/<split>/<nome>.txt
    destino.write_text(rotulos[img.stem].strip() + "\n")
print(f"{len(imagens) - len(faltando)} rotulos gravados; sem rotulo: {faltando or 'nenhuma'}")
