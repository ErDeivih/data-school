"""exportar-y-servir-modelos-1.py — de qué está hecha la diferencia entre el modelo que entrenas
y el modelo que sirve: orden de acumulación, precisión al guardar y cuello de botella de memoria.
La figura de la página de exportar y servir modelos."""

import numpy as np

from comun import *

estilo()

rng = np.random.default_rng(0)


def suma_secuencial(x):
    """Suma en orden, en float32: como lo haría una implementación ingenua, un sumando cada vez."""
    total = np.float32(0.0)
    for v in x:
        total = np.float32(total + v)
    return float(total)


# --- Panel 1: la misma suma, dos órdenes ---------------------------------------
tamanos = [1000, 3000, 10000, 30000, 100000, 300000]
errores = []
for n in tamanos:
    x = (0.1 + rng.normal(0, 0.01, n)).astype(np.float32)
    secuencial = suma_secuencial(x)
    parejas = float(np.sum(x))                     # NumPy suma por parejas, no en orden
    errores.append(abs(secuencial - parejas) / parejas)

# --- Panel 2: error de reconstrucción al bajar de precisión --------------------
W = rng.normal(0.0, 0.05, size=(128, 128))


def reconstruir(W, bits):
    """Cuantización simétrica por tensor con `bits` bits, como la de un export a int8/int4."""
    qmax = 2 ** (bits - 1) - 1
    escala = np.abs(W).max() / qmax
    return np.clip(np.round(W / escala), -qmax - 1, qmax) * escala


def error_relativo(W, reconstruido):
    return float(np.sqrt(((W - reconstruido) ** 2).mean()) / W.std())


precisiones = [
    ("float32", error_relativo(W, W.astype(np.float32).astype(np.float64))),
    ("float16", error_relativo(W, W.astype(np.float16).astype(np.float64))),
    ("int8", error_relativo(W, reconstruir(W, 8))),
    ("int4", error_relativo(W, reconstruir(W, 4))),
    ("int3", error_relativo(W, reconstruir(W, 3))),
]

fig, ejes = plt.subplots(2, 1, figsize=(8.6, 7.4))

# --- Arriba: el orden de la suma cambia el ultimo bit --------------------------
ejes[0].loglog(tamanos, errores, color=AZUL, linewidth=1.8, marker="o", markersize=4)
# El texto va en la esquina inferior derecha, que está vacía: la curva sube hacia arriba a la
# derecha y una nota en esa zona cruzaría la línea con una flecha larga.
anotar(ejes[0], "el error se queda en el último bit", xy=(tamanos[1], errores[1]),
       xytext=(0.30, 0.12), color=TEXTO, flecha=False)
ejes[0].set_xlabel("número de sumandos")
ejes[0].set_ylabel("error relativo")
titulo(ejes[0], "Reordenar una suma en float32 la cambia",
       "por eso el modelo exportado no da exactamente los mismos números")
rejilla(ejes[0], "both")
numeros(ejes[0], "both")

# --- Abajo: qué cuesta bajar de precisión -------------------------------------
nombres = [p[0] for p in precisiones]
valores = [p[1] for p in precisiones]
colores = [VERDE, CIAN, NARANJA, ROJO, MORADO]
barras = ejes[1].bar(nombres, [v * 100 for v in valores], color=colores, width=0.6)
for barra, v in zip(barras, valores):
    ejes[1].text(barra.get_x() + barra.get_width() / 2, v * 100, f"{v * 100:.3f} %",
                 ha="center", va="bottom", fontsize=8.5, color=TEXTO)
ejes[1].set_ylabel("error sobre la desviación de los pesos (%)")
ejes[1].set_ylim(0, max(valores) * 100 * 1.22)
titulo(ejes[1], "Cada precisión tiene su precio en error",
       "float16 no se nota; int4 hay que compensarlo con escala por canal o calibración")
rejilla(ejes[1])
numeros(ejes[1], "y")

guardar(fig, "exportar-servir-acumulacion-y-precisión")

print("errores por tamaño", [f"{e:.2e}" for e in errores])
print("error relativo por precisión", [(n, f"{v:.6f}") for n, v in precisiones])
# float32 pierde entre 1e-7 y 1e-6 de precisión relativa en una multiplicación larga: eso es
# justo el orden de magnitud de la diferencia entre el modelo de PyTorch y el exportado.
W32 = W.astype(np.float32)
error_mm = float(np.abs((W32 @ W32.T).astype(np.float64) - W @ W.T).max()
                 / np.abs(W @ W.T).max())
print("multiplicación en float32 contra float64, error relativo máximo", f"{error_mm:.2e}")
print("tamaño de los pesos", W.nbytes, "bytes en float64 y", W32.nbytes, "en float32")

