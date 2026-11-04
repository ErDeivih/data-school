import numpy as np

rng = np.random.default_rng(0)
ret = np.concatenate([rng.normal(0.0002, 0.005, size=120),   # 120 dias tranquilos
                      rng.normal(-0.0020, 0.025, size=40)])  # 40 dias de panico
objetivo = 0.10        # volatilidad objetivo, en tanto por uno

# Dimensionar con la volatilidad de toda la serie usa datos que en ese dia no existian.
vol_total = ret.std(ddof=1)
vol_pasado = np.array([ret[:t].std(ddof=1) if t >= 5 else np.nan
                       for t in range(ret.size)])

for t in (10, 150):
    print(f"t={t:>3}  tamano con vol total {objetivo / vol_total:.1f}  "
          f"con vol solo-pasado {objetivo / vol_pasado[t]:.1f}")
# en t=10 la vol total pide 7.6 y la informacion disponible pedia 25.6

diferencia = np.abs(objetivo / vol_total - objetivo / vol_pasado) / (objetivo / vol_pasado)
print(f"dias con tamano distinto mas del 20 %: {int((diferencia > 0.20).sum())} de {ret.size}")
# -> 134 de 160
