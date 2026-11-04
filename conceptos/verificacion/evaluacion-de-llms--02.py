import numpy as np

# Etiquetas de un juez automatico y de un anotador humano sobre 50 respuestas.
juez = np.array([1] * 30 + [0] * 20)
humano = np.array([1] * 28 + [0] * 2 + [1] * 2 + [0] * 18)

# .mean() de un array de 0 y 1 es la proporcion de unos; comparar arrays da True/False
acuerdo = float((juez == humano).mean())
pj, ph = juez.mean(), humano.mean()
esperado = pj * ph + (1 - pj) * (1 - ph)      # acuerdo que daria el puro azar
kappa = (acuerdo - esperado) / (1 - esperado)

print("acuerdo observado:", round(acuerdo, 2))
print("acuerdo por azar :", round(float(esperado), 3))
print("kappa            :", round(float(kappa), 2))
# (juez != humano).sum() cuenta las posiciones donde discrepan: 4 de 50
print("desacuerdos      :", int((juez != humano).sum()), "de", juez.size)
