import numpy as np

# Simulacion con apuesta de tamano fijo: cada operacion suma o resta `riesgo`
# unidades del capital inicial (no se reajusta el tamano al capital actual).
rng = np.random.default_rng(7)
n_ops, n_caminos = 200, 20_000
resultados = rng.choice([1.0, -1.0], size=(n_caminos, n_ops), p=[0.55, 0.45])

for riesgo in (0.02, 0.10):
    capital = 1 + riesgo * np.cumsum(resultados, axis=1)
    ruina_total = (capital <= 0).any(axis=1)
    caida_mitad = (capital <= 0.5).any(axis=1)
    print(f"riesgo {riesgo:>4.0%}  ruina {ruina_total.mean():6.2%}  caida del 50% {caida_mitad.mean():6.2%}")
# -> riesgo   2%  ruina  0.00%  caida del 50%  0.31%
# -> riesgo  10%  ruina 11.83%  caida del 50% 35.11%
