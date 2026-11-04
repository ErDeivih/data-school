"""covarianza-y-correlacion-1.py — que mide de verdad la correlación y que deja fuera.

Izquierda: dos variables con relación lineal fuerte, con la covarianza y la correlación
escritas al lado. Centro: una relación perfecta (y = x^2) cuya correlación es cero, que es la
trampa clasica. Abajo: cuanto baja la volatilidad de una cartera segun la correlación.

Los tres paneles van en DOS FILAS (dos arriba y el de la cartera ocupando el ancho de abajo):
en una sola fila cada panel quedaba tan estrecho que las notas se salian y se pisaban.
"""

import numpy as np

from comun import *

estilo()

azar = np.random.default_rng(7)

fig = plt.figure(figsize=(10.4, 7.8))
rejilla_paneles = fig.add_gridspec(2, 2)
ejes = [fig.add_subplot(rejilla_paneles[0, 0]),
        fig.add_subplot(rejilla_paneles[0, 1]),
        fig.add_subplot(rejilla_paneles[1, :])]

# --- Panel 1: relacion lineal, la covarianza depende de las unidades --------------
horas = np.array([1, 2, 3, 4, 5, 6], dtype=float)
notas = np.array([4.0, 4.5, 5.0, 6.0, 7.0, 8.5])
cov = float(np.cov(horas, notas, ddof=1)[0, 1])
r = float(np.corrcoef(horas, notas)[0, 1])
assert abs(cov - 3.1) < 1e-9 and abs(r - 0.9787) < 1e-3

pendiente = cov / float(horas.var(ddof=1))
ejes[0].scatter(horas, notas, s=34, color=AZUL, zorder=3)
ejes[0].plot(horas, notas.mean() + pendiente * (horas - horas.mean()), color=ROJO, linewidth=1.5)
# La nube sube de abajo a la izquierda a arriba a la derecha, asi que el hueco de arriba a
# la izquierda queda libre para los dos numeros.
# Las etiquetas se montan con % y NO con f-string a proposito: el corrector de tildes de las
# figuras protege las expresiones {...} con un centinela y no siempre lo borra, y esos bytes
# sueltos salen luego como cuadraditos en el SVG (incidente del 2026-10-15).
ejes[0].text(0.05, 0.95, ("covarianza = %.2f" % cov).replace(".", ","),
             transform=ejes[0].transAxes, va="top", color=TEXTO, fontsize=9.5)
ejes[0].text(0.05, 0.86, ("correlación = %.4f" % r).replace(".", ","),
             transform=ejes[0].transAxes, va="top", color=ROJO, fontsize=9.5)
titulo(ejes[0], "Lineal: la nube se aprieta en una recta",
       "si las notas pasaran a escala 0-100, la covarianza seria 310 y r seguiria igual")
ejes[0].set_xlabel("horas de estudio")
ejes[0].set_ylabel("nota")
numeros(ejes[0])
rejilla(ejes[0])

# --- Panel 2: dependencia perfecta con correlacion cero ---------------------------
x = np.linspace(-3, 3, 200)
ejes[1].plot(x, x ** 2, color=MORADO, linewidth=1.6)
puntos = np.arange(-3, 4, dtype=float)
ejes[1].scatter(puntos, puntos ** 2, s=30, color=MORADO, zorder=3)
# La nota va dentro del hueco que dejan los dos brazos de la parabola, no encima del
# brazo izquierdo, que era donde caia antes.
anotar(ejes[1], "correlación de x con x^2 = 0,0000", xy=(0.0, 0.0), xytext=(0.26, 0.82),
       color=MORADO)
ejes[1].axhline(0, color=REJILLA, linewidth=0.9, linestyle=":")
titulo(ejes[1], "Dependencia total y correlación cero",
       "saber x determina y sin ningun error, y sin embargo la correlación es cero")
ejes[1].set_xlabel("x")
ejes[1].set_ylabel("y = x^2")
numeros(ejes[1])
rejilla(ejes[1])

# --- Panel 3: que compra la correlacion negativa en una cartera -------------------
pesos = np.array([0.6, 0.4])
sigmas = np.array([0.20, 0.10])
rhos = np.linspace(-1, 1, 200)
varianzas = (pesos ** 2 * sigmas ** 2).sum() + 2 * pesos[0] * pesos[1] * rhos * sigmas[0] * sigmas[1]
volatilidades = np.sqrt(varianzas)
ingenua = float((pesos * sigmas).sum())


def vol_en(rho):
    var = float((pesos ** 2 * sigmas ** 2).sum()
                + 2 * pesos[0] * pesos[1] * rho * sigmas[0] * sigmas[1])
    return np.sqrt(var)


ejes[2].plot(rhos, volatilidades * 100, color=VERDE, linewidth=1.8)
ejes[2].axhline(ingenua * 100, color=ROJO, linewidth=1.3, linestyle="--")
# Con el eje un poco mas alto que los datos, la etiqueta de la linea roja cabe DENTRO del
# panel (antes se salia por arriba y se cruzaba con el titulo) y las dos notas de los
# puntos caen, una sobre la curva y otra debajo, sin pisarse entre ellas.
ejes[2].set_ylim(7.0, 18.2)
for rho_marca in (-0.3, 0.3):
    v = float(vol_en(rho_marca) * 100)
    ejes[2].scatter([rho_marca], [v], s=34, color=VERDE, zorder=3)
    # Cada etiqueta va a un lado distinto del punto, para que ninguna caiga sobre la curva
    # ni sobre la otra.
    etiqueta = (("rho = %+.1f" % rho_marca).replace(".", ",")
                + ("\nsigma = %.1f %%" % v).replace(".", ","))
    anotar(ejes[2], etiqueta, xy=(rho_marca, v),
           xytext=(0.06, 0.46) if rho_marca < 0 else (0.74, 0.50), color=VERDE)
anotar(ejes[2], "media ponderada de volatilidades: %s %%" % coma(round(ingenua * 100, 1)),
       xy=(0.75, ingenua * 100), xytext=(0.28, 0.94), color=ROJO)
titulo(ejes[2], "La correlación cambia el riesgo, no el retorno",
       "el retorno esperado es el mismo; lo que cambia es cuanto se mueve la cartera")
ejes[2].set_xlabel("correlación entre los dos activos")
ejes[2].set_ylabel("volatilidad de la cartera (%)")
numeros(ejes[2])
rejilla(ejes[2])

guardar(fig, "correlacion-lineal-cero-y-cartera")
