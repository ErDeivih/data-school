import numpy as np

# La misma media en dos generaciones distintas: los ingresos no son simetricos.
rng = np.random.default_rng(1)
normal = rng.normal(50_000.0, 20_000.0, size=100_000)
lognormal = rng.lognormal(mean=10.8, sigma=0.6, size=100_000)

for nombre, muestra in (("normal", normal), ("lognormal", lognormal)):
    limite = muestra.mean() + 3 * muestra.std()
    print(nombre, "media", round(float(muestra.mean())),
          "mediana", round(float(np.median(muestra))),
          "maximo", round(float(muestra.max())),
          "fuera de 3 sigma", int((muestra > limite).sum()))
