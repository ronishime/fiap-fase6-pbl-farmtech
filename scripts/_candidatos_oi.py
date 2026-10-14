"""Seleciona candidatos do Open Images V7 (vaca e trator) a partir dos CSVs de metadados."""
import sys, pandas as pd
meta = sys.argv[1]
CATTLE, TRACTOR = "/m/01xq0k1", "/m/013xlm"
# rotulos de imagem verificados por humanos (val + test)
lab = pd.concat([pd.read_csv(f"{meta}/oidv7-{s}-annotations-human-imagelabels.csv") for s in ("val", "test")])
pos = lab[lab.Confidence == 1]
has = lambda m: set(pos.loc[pos.LabelName == m, "ImageID"])
cattle_img, tractor_img = has(CATTLE), has(TRACTOR)
print("imagens com vaca:", len(cattle_img), "| com trator:", len(tractor_img), "| ambos:", len(cattle_img & tractor_img))
# caixas (apenas classes boxable) val + test
bb = pd.concat([pd.read_csv(f"{meta}/{s}-annotations-bbox.csv") for s in ("validation", "test")])
cb = bb[bb.LabelName == CATTLE].copy()
cb["area"] = (cb.XMax - cb.XMin) * (cb.YMax - cb.YMin)
g = cb.groupby("ImageID").agg(n=("area", "size"), amax=("area", "max"), grp=("IsGroupOf", "max"),
                              dep=("IsDepiction", "max"), trunc=("IsTruncated", "mean"))
# vaca: sem caixa de grupo, sem desenho, 1-4 animais, maior animal >= 8% da imagem, sem trator
ok_c = g[(g.grp == 0) & (g.dep == 0) & (g.n <= 4) & (g.amax >= 0.08)]
ok_c = ok_c[~ok_c.index.isin(tractor_img)]
print("vacas candidatas:", len(ok_c))
# trator: sem vaca; sem caixa de Cattle
ok_t = sorted(tractor_img - cattle_img - set(cb.ImageID))
print("tratores candidatos:", len(ok_t))
info = pd.concat([pd.read_csv(f"{meta}/{s}-images-with-rotation.csv") for s in ("validation", "test")]).set_index("ImageID")
oc = info.loc[ok_c.index].assign(classe="vaca", n_obj=ok_c.n, amax=ok_c.amax)
ot = info.loc[ok_t].assign(classe="trator")
out = pd.concat([oc, ot])
# so licencas CC BY (2.0) e imagens sem rotacao estranha
print(out.License.value_counts())
out = out[out.Rotation.fillna(0) == 0]
out.to_csv(f"{meta}/candidatos.csv")
cb[cb.ImageID.isin(ok_c.index)].to_csv(f"{meta}/caixas_vaca.csv", index=False)
print(out.groupby(["classe", "Subset"]).size())
