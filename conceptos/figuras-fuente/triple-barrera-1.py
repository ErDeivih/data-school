"""triple-barrera-1.py — la etiqueta depende del camino, no del destino. A la izquierda, dos
series que acaban en el mismo precio y reciben etiquetas opuestas; a la derecha, el reparto
de las tres clases que sale al etiquetar por barreras y por umbral fijo, que no es el mismo.

Página del etiquetado por triple barrera (fase 9)."""

import numpy as np

from comun import *

estilo()


def etiqueta_triple_barrera(precios, t0, sigma, pt=1.0, sl=1.0, h=6, escala=1.0):
    """Devuelve la etiqueta y la barra en que queda determinada, t1.

    `escala` ensancha las dos barreras: con 1 se usan pt y sl volatilidades por barra, y
    con √h se usan pt y sl volatilidades del horizonte entero."""
    p0 = precios[t0]
    arriba = p0 * (1 + pt * sigma * escala)
    abajo = p0 * (1 - sl * sigma * escala)
    for t in range(t0 + 1, min(t0 + h + 1, precios.size)):
        if precios[t] >= arriba:
            return 1, t
        if precios[t] <= abajo:
            return -1, t
    return 0, min(t0 + h, precios.size - 1)


# ── Izquierda: dos caminos con el mismo destino ───────────────────────────────
camino_a = np.array([100.0, 101.0, 102.5, 103.2, 104.0])
camino_b = np.array([100.0, 99.0, 97.5, 101.0, 104.0])
arriba, abajo = 102.0, 98.0
t = np.arange(5)

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.4))

eje = ejes[0]
eje.axhspan(arriba, 105.6, color=VERDE, alpha=0.10)
eje.axhspan(94.4, abajo, color=ROJO, alpha=0.10)
eje.axhline(arriba, color=VERDE, linewidth=1.4)
eje.axhline(abajo, color=ROJO, linewidth=1.4)
eje.axhline(100.0, color=REJILLA, linewidth=1.1, linestyle=":")
eje.plot(t, camino_a, color=VERDE, linewidth=2.0, marker="o", markersize=5,
         label="camino A: toca el objetivo")
eje.plot(t, camino_b, color=ROJO, linewidth=2.0, marker="s", markersize=5,
         label="camino B: toca el stop")
eje.text(4.02, camino_a[-1] + 0.22, "+1", fontsize=10, color=VERDE, ha="left", va="center")
eje.text(4.02, camino_b[-1] - 0.30, "−1", fontsize=10, color=ROJO, ha="left", va="center")
eje.text(0.04, 105.0, "barrera de beneficio: 102,00", fontsize=8.5, color=VERDE)
eje.text(0.04, 94.8, "barrera de pérdida: 98,00", fontsize=8.5, color=ROJO)
eje.set_ylim(94.4, 105.6)
eje.set_xlim(-0.2, 4.5)
anotar(eje, "mismo destino, +4 % en las dos:\nla etiqueta la decide el camino",
       xy=(1.0, 99.0), xytext=(0.20, 0.22), color=MORADO, flecha=False)
titulo(eje, "Dos caminos, un destino, etiquetas opuestas",
       "La que se cierra en el stop ya no cobra el beneficio posterior")
eje.set_xticks(t)
eje.set_xlabel("barra desde el evento")
eje.set_ylabel("precio")
eje.legend(loc="lower right", fontsize=8)
rejilla(eje)
numeros(eje, "y")

# ── Derecha: el reparto de clases según lo ancho que pongas el stop ───────────
azar = np.random.default_rng(7)
n, sigma, h = 4000, 0.02, 20
precios = 100.0 * np.exp(np.cumsum(azar.normal(0.0002, sigma, n)))

variantes = [("1 σ diaria", 1.0), ("1 σ · √h", np.sqrt(h))]
clases = [-1, 0, 1]
series = []
for nombre_variante, escala in variantes:
    por_barrera, por_umbral = [], []
    for t0 in range(0, n - h - 2, 3):
        etq, _ = etiqueta_triple_barrera(precios, t0, sigma, h=h, escala=escala)
        por_barrera.append(etq)
        # El etiquetado de manual: el signo del retorno a horizonte fijo, sin barreras.
        por_umbral.append(int(np.sign(precios[t0 + h] - precios[t0])))
    series.append((nombre_variante,
                   100 * np.array([por_barrera.count(k) for k in clases]) / len(por_barrera),
                   100 * np.array([por_umbral.count(k) for k in clases]) / len(por_umbral)))

eje = ejes[1]
ancho = 0.36
etiquetas_x = []
for i, (nombre_variante, proporcion_barrera, proporcion_fija) in enumerate(series):
    base = i * 3
    eje.bar(np.arange(base, base + 3) - ancho / 2, proporcion_barrera, width=ancho,
            color=AZUL if i == 0 else CIAN,
            label="triple barrera" if i == 0 else None)
    eje.bar(np.arange(base, base + 3) + ancho / 2, proporcion_fija, width=ancho,
            color=NARANJA if i == 0 else ROSA,
            label="signo del retorno a 20 barras" if i == 0 else None)
    for j, (vb, vf) in enumerate(zip(proporcion_barrera, proporcion_fija)):
        eje.text(base + j - ancho / 2, vb + 1.4, f"{vb:.0f} %".replace(".", ","),
                 ha="center", fontsize=8, color=AZUL if i == 0 else CIAN)
        eje.text(base + j + ancho / 2, vf + 1.4, f"{vf:.0f} %".replace(".", ","),
                 ha="center", fontsize=8, color=NARANJA if i == 0 else ROSA)
    etiquetas_x += [f"{nombre_variante}\n+1", f"{nombre_variante}\n0",
                    f"{nombre_variante}\n−1"]
eje.set_xticks(np.arange(6))
eje.set_xticklabels(etiquetas_x, fontsize=8)
anotar(eje, "con barreras de 1 σ diaria no hay clase 0:\nel precio siempre toca una de las dos",
       xy=(1, 1.5), xytext=(0.03, 0.86), color=ROJO, flecha=False)
eje.set_ylim(0, 92)
titulo(eje, "El tiempo también es una barrera",
       "Etiquetas de 1 300 eventos simulados, según el ancho de las barreras")
eje.set_xlabel("etiqueta, por variante de barreras")
eje.set_ylabel("% de las observaciones")
eje.legend(loc="upper right", fontsize=7.5)
rejilla(eje)
numeros(eje, "y")

guardar(fig, "triple-barrera-camino-y-reparto-de-clases")
