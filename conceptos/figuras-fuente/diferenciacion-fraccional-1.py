"""diferenciacion-fraccional-1.py — el compromiso del orden d: memoria que se conserva
frente a estacionariedad. Figura de la pagina de diferenciación fraccional (fase 9)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(0)


def pesos_fracd(d, umbral=1e-3):
    """Pesos w_k de (1-B)^d, truncados cuando el valor absoluto baja del umbral."""
    w, k = [1.0], 1
    while True:
        s = -w[-1] * (d - k + 1) / k
        if abs(s) < umbral:
            break
        w.append(s)
        k += 1
    return np.array(w)


def acf(x, lag):
    x = x - x.mean()
    return float(np.dot(x[:-lag], x[lag:]) / np.dot(x, x))


# Un paseo con deriva (no estacionario) y sus versiones diferenciadas con tres ordenes.
# La semilla y el tamano son los del ejemplo de la pagina, para que los numeros coincidan.
serie = np.cumsum(azar.normal(0.05, 1.0, 800))
rezagos = np.arange(1, 41)
memoria = {}
for d in (0.0, 0.4, 1.0):
    if d == 0.0:
        y = serie
    else:
        w = pesos_fracd(d)
        y = np.convolve(serie, w, "full")[w.size - 1:][-700:]
    memoria[d] = np.array([acf(y, k) for k in rezagos])

v04, v1 = memoria[0.4][24], memoria[1.0][24]
banda = 1.96 / np.sqrt(700)

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 6.4))

# --- Arriba: cuanta memoria queda a cada distancia ------------------------------------
ejes[0].axhspan(-banda, banda, color=CIAN, alpha=0.15)
for d, color in ((0.0, MORADO), (0.4, AZUL), (1.0, VERDE)):
    ejes[0].plot(rezagos, memoria[d], color=color, linewidth=1.8)
ejes[0].axhline(0, color=TEXTO, linewidth=0.8, alpha=0.4)
ejes[0].axvline(25, color=REJILLA, linewidth=1.0, linestyle="--")
ejes[0].set_ylim(-0.35, 1.26)
titulo(ejes[0], "Qué queda del pasado según el orden de diferenciación",
       "morado: sin diferenciar · azul: d = 0,4 · verde: d = 1 (el retorno de siempre)")
anotar(ejes[0], "sin diferenciar no es estacionaria", xy=(8, 0.98),
       xytext=(0.02, 0.95), color=MORADO, flecha=False)
anotar(ejes[0], f"a 25 rezagos, con d = 0,4 todavía vale {v04:.3f} y con d = 1 vale {v1:.3f}".replace(".", ","),
       xy=(25, v04), xytext=(0.98, 0.45), color=AZUL, align="right")
anotar(ejes[0], "banda de ruido: por debajo de aquí ya no hay memoria",
       xy=(30, 0.0), xytext=(0.98, 0.09), color=CIAN, align="right", flecha=False)
ejes[0].set_xlabel("rezagos")
ejes[0].set_ylabel("autocorrelación")
rejilla(ejes[0], "both")
numeros(ejes[0])

# --- Abajo: el residuo de la suma de pesos es la memoria que se conserva --------------
ds = np.linspace(0.02, 1.0, 140)
sumas = np.array([pesos_fracd(d).sum() for d in ds])
w04 = pesos_fracd(0.4)
ejes[1].plot(ds, sumas, color=MORADO, linewidth=1.9)
ejes[1].axvline(0.4, color=AZUL, linewidth=1.3, linestyle=":")
ejes[1].plot([0.4], [w04.sum()], marker="o", markersize=6, color=AZUL)
ejes[1].set_ylim(-0.05, 1.35)
ejes[1].set_xlabel("orden de diferenciación d")
ejes[1].set_ylabel("suma de los pesos")
titulo(ejes[1], "Cuanto más pequeño es d, más nivel sobrevive en la serie",
       f"suma de los {w04.size} pesos truncados (τ = 10⁻³): ese residuo es la memoria conservada")
anotar(ejes[1], "d pequeño: mucha memoria,\npero puede no ser estacionaria",
       xy=(0.06, 0.95), xytext=(0.02, 0.94), color=ROJO, flecha=False)
anotar(ejes[1], f"d = 0,4: {w04.sum():.3f} del nivel".replace(".", ","),
       xy=(0.4, w04.sum()), xytext=(0.52, 0.52), color=AZUL)
anotar(ejes[1], "d = 1: la suma es 0 exacto,\nla primera diferencia tira el nivel entero",
       xy=(1.0, 0.0), xytext=(0.98, 0.34), color=VERDE, align="right")
rejilla(ejes[1], "both")
numeros(ejes[1])

guardar(fig, "fracdiff-memoria-y-nivel")
