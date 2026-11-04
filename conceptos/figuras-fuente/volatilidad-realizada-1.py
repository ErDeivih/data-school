"""volatilidad-realizada-1.py — la volatilidad realizada ve el camino, no solo el cierre,
y el rebote bid-ask la infla si muestreas demasiado fino. Figura de la página de
volatilidad realizada (fase 9)."""

import numpy as np

from comun import *

estilo()

azar = np.random.default_rng(7)

# ── Panel de arriba: dos estimadores del mismo día ─────────────────────────────
precios = np.array([100.00, 100.35, 100.10, 99.45, 98.95, 99.15, 99.75,
                    100.45, 100.85, 100.30, 100.05, 100.00])
r = np.diff(np.log(precios))
rv_recorrido = float(np.sum(r ** 2))
rv_cierre = float(np.log(precios[-1] / precios[0]) ** 2)

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 5.8))

eje = ejes[0]
eje.plot(precios, color=AZUL, linewidth=1.9)
eje.fill_between(range(len(precios)), precios, precios.min() - 0.05,
                 color=AZUL, alpha=0.08)
eje.axhline(precios[0], color=TEXTO, linewidth=0.9, linestyle="--")
titulo(eje, "Un día que acaba donde empezó puede haber sido violento",
       "La línea de puntos es el precio de apertura: el retorno de cierre es exactamente cero")
eje.set_xlabel("precio intradía, tomado cada media hora")
eje.set_ylabel("precio")
eje.set_ylim(precios.min() - 0.12, precios.max() + 0.12)
eje.set_xticks(range(len(precios)))
rejilla(eje)
anotar(eje, f"varianza realizada del camino: {rv_recorrido:.2e}",
       (7, precios[7]), (0.30, 0.36), color=AZUL)
anotar(eje, "la del cierre a cierre: cero, el día parece tranquilo",
       (1, precios[1]), (0.04, 0.80), color=ROJO, flecha=False)

# ── Panel de abajo: muestrear más fino añade ruido, no información ─────────────
# 4.000 sesiones de 60 minutos. El precio eficiente se mueve 5 pb por minuto; encima
# lleva un rebote bid-ask de 2 pb, independiente y sin información. Se mide la
# varianza realizada muestreando el precio cada `factor` minutos.
dias, minutos = 20000, 60
pasos = azar.normal(0, 0.0005, (dias, minutos))
log_limpio = np.concatenate([np.zeros((dias, 1)), np.cumsum(pasos, axis=1)], axis=1)
ruido = 0.0002 * azar.choice([-1.0, 1.0], (dias, minutos + 1))
log_observado = log_limpio + ruido

factores = np.array([1, 2, 3, 5, 10, 15, 20, 30, 60])
rv_limpia, rv_observada = [], []
for factor in factores:
    indices = np.arange(0, minutos + 1, factor)
    retorno_limpio = np.diff(log_limpio[:, indices], axis=1)
    retorno_observado = np.diff(log_observado[:, indices], axis=1)
    rv_limpia.append(float(np.mean(np.sum(retorno_limpio ** 2, axis=1))))
    rv_observada.append(float(np.mean(np.sum(retorno_observado ** 2, axis=1))))
rv_limpia, rv_observada = np.array(rv_limpia), np.array(rv_observada)

eje = ejes[1]
eje.axhline(1.0, color=VERDE, linewidth=2.0,
            label="la varianza que de verdad hubo")
eje.plot(factores, rv_observada / rv_limpia, color=ROJO, linewidth=1.9,
         marker="o", markersize=4, label="lo que mide la varianza realizada")
eje.axvline(5, color=MORADO, linewidth=1.2, linestyle=":")
titulo(eje, "Muestrear más fino añade ruido, no información",
       "Varianza realizada de 20.000 sesiones, en unidades de la varianza verdadera")
eje.set_xlabel("minutos por barra (hacia la derecha el muestreo es más grueso)")
eje.set_ylabel("varianza medida\n/ varianza verdadera")
eje.set_xlim(0, 62)
eje.set_ylim(0.96, 1.40)
rejilla(eje)
eje.legend(loc="upper right", fontsize=8)
anotar(eje, f"al minuto sale un {100*(rv_observada[0]/rv_limpia[0]-1):.0f} % "
            f"por encima de la real",
       (1, rv_observada[0] / rv_limpia[0]), (0.12, 0.66), color=ROJO)
anotar(eje, f"a los 5 minutos el sesgo cae al "
            f"{100*(rv_observada[3]/rv_limpia[3]-1):.0f} % de la varianza verdadera",
       (5, rv_observada[3] / rv_limpia[3]), (0.30, 0.20), color=MORADO)

numeros(ejes[1])

guardar(fig, "volatilidad-realizada-camino-y-sesgo")
