"""descomposicion-stl-1.py — separar la serie en tres trozos que se suman.

Arriba, la serie tal como se ve. Debajo, los tres componentes: la tendencia que no vuelve a empezar,
el patron estacional que se repite y el residuo, que es lo único que hay que mirar cuando algo va
mal. La figura de la pagina de descomposición STL (fase 5).

Los cuatro titulos van cortos y cada nota explica su panel: en cuatro filas apiladas un titulo de
dos lineas se come el eje de arriba y la rejilla de al lado."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

n = 72
t = np.arange(n)
trimestre = t % 4
patron_real = np.array([4.0, 0.0, -3.0, -1.0])          # la estacionalidad verdadera
tendencia_real = 50 + 0.5 * t
y = tendencia_real + patron_real[trimestre] + azar.normal(0, 1.2, n)


def descomponer(serie, m=4):
    """Clasica: tendencia por media movil centrada 2xm y estacionalidad por fases."""
    pesos = np.concatenate([[0.5], np.ones(m - 1), [0.5]]) / m
    tend = np.full(serie.size, np.nan)
    for i in range(serie.size - m):
        tend[i + m // 2] = pesos @ serie[i:i + m + 1]
    sin_tend = serie - tend
    fase = np.array([np.nanmean(sin_tend[k::m]) for k in range(m)])
    est = np.tile(fase - fase.mean(), serie.size // m + 1)[:serie.size]
    return tend, est, serie - tend - est


tend, est, resid = descomponer(y)
desviacion = float(np.nanstd(resid))

fig, ejes = plt.subplots(4, 1, figsize=(8.6, 7.4), sharex=True)

# --- La serie observada -------------------------------------------------------
ejes[0].plot(t, y, color=AZUL, linewidth=1.5)
titulo(ejes[0], "La serie observada")
ejes[0].set_ylabel("ventas")
rejilla(ejes[0])
numeros(ejes[0])
# La nota va donde la curva no llega: a la derecha la serie sube hasta 85 y aqui abajo no pasa
# de 48, asi que el texto cae en zona vacia sin rectangulo blanco.
anotar(ejes[0], "los tres componentes mezclados:\nlo de debajo hay que reconstruirlo",
      xy=(30, y[30]), xytext=(0.60, 0.16), color=TEXTO, flecha=False)

# --- La tendencia -------------------------------------------------------------
ejes[1].plot(t, y, color=REJILLA, linewidth=0.9)
ejes[1].plot(t, tend, color=NARANJA, linewidth=2.0)
titulo(ejes[1], "La tendencia")
ejes[1].set_ylabel("nivel de fondo")
rejilla(ejes[1])
numeros(ejes[1])
# Esquina inferior derecha: alli la serie ya ha subido a 82 y deja el hueco libre.
anotar(ejes[1], "una media movil centrada de un ciclo entero:\n"
                "promedia 4 trimestres y pierde los extremos",
      xy=(55, tend[55]), xytext=(0.97, 0.12), color=NARANJA, flecha=False, align="right")

# --- La estacionalidad --------------------------------------------------------
ejes[2].plot(t, est, color=VERDE, linewidth=1.2, zorder=1)
ejes[2].plot(np.arange(0, n, 4), est[0::4], color=ROJO, linewidth=0, marker="o", markersize=6,
             zorder=3)
ejes[2].axhline(0, color=TEXTO, linewidth=0.8, alpha=0.4)
titulo(ejes[2], "La estacionalidad")
ejes[2].set_ylabel("efecto del trimestre")
# Se deja mas aire por arriba que por abajo: los picos llegan a 4 y las dos notas caben en esa
# franja libre, sin tocar la sierra verde ni los puntos rojos.
ejes[2].set_ylim(est.min() - 1.4, est.max() + 2.6)
rejilla(ejes[2])
numeros(ejes[2])
anotar(ejes[2], "los puntos rojos abren cada ciclo:\nel pico cae siempre en el mismo sitio",
      xy=(8, est[8]), xytext=(0.97, 0.94), color=ROJO, flecha=False, align="right")
# La sierra cruza todo el panel, asi que la unica franja limpia es la de abajo a la derecha,
# que es tambien donde el limite inferior deja sitio.
anotar(ejes[2], "media cero dentro de cada ciclo:\nsi no, se confundiria con la tendencia",
      xy=(4, est[1]), xytext=(0.97, 0.05), color=VERDE, flecha=False, align="right")

# --- El residuo ---------------------------------------------------------------
ejes[3].plot(t, resid, color=ROJO, linewidth=1.3, zorder=3)
ejes[3].axhline(0, color=TEXTO, linewidth=0.8, alpha=0.4)
ejes[3].axhline(2 * desviacion, color=REJILLA, linewidth=1.0, linestyle="--")
ejes[3].axhline(-2 * desviacion, color=REJILLA, linewidth=1.0, linestyle="--")
ejes[3].set_title("El residuo: lo que no explican los otros dos")
ejes[3].set_xlabel("trimestre")
ejes[3].set_ylabel("residuo")
ejes[3].set_ylim(-2.9, 3.3)
rejilla(ejes[3])
numeros(ejes[3])
peor = int(np.nanargmax(np.abs(resid)))
# La nota de las rayas va pegada al borde de arriba y la del dato raro al de abajo: asi las dos
# caen en las franjas que la serie no visita (por encima de 1,3 y por debajo de -1,3).
ejes[3].text(0.97, 0.97, "rayas: dos desviaciones del propio residuo",
             transform=ejes[3].transAxes, fontsize=8.5, color=REJILLA, ha="right", va="top")
anotar(ejes[3], "el punto más grande es el candidato a\ndato mal cargado, no a movimiento del negocio",
      xy=(peor, resid[peor]), xytext=(0.97, 0.22), color=ROJO, flecha=False, align="right")

guardar(fig, "descomposicion-stl-tres-componentes")
