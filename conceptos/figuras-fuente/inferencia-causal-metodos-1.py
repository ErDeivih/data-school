"""inferencia-causal-metodos-1.py — dos de los cuatro disenos, vistos por dentro.

Izquierda: diferencias en diferencias. Los dos grupos se mueven en paralelo hasta la reforma;
después, la distancia entre lo que paso y lo que habria pasado sin programa es el efecto.
Derecha: regresión discontinua. El salto de la nube justo en el corte es el efecto, porque a
cada lado del corte los individuos son comparables.
La figura de la pagina de metodos de inferencia causal (fase 2)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

fig, ejes = plt.subplots(1, 2, figsize=(10.2, 4.4))

# --- Panel 1: diferencias en diferencias ---------------------------------------------
anios = np.array([-2.0, -1.0, 1.0, 2.0])
tratado = np.array([18.5, 20.0, 26.0, 26.9])
control = np.array([8.5, 10.0, 12.0, 12.9])
contrafactual_x = np.array([-1.0, 1.0, 2.0])
contrafactual_y = np.array([20.0, 22.0, 22.9])       # el tratado, sin el programa

ejes[0].axvline(0, color=REJILLA, linewidth=1.1, linestyle=":")
ejes[0].plot(anios, tratado, color=AZUL, linewidth=2.0, marker="o", markersize=5, zorder=3)
ejes[0].plot(anios, control, color=VERDE, linewidth=2.0, marker="o", markersize=5, zorder=3)
ejes[0].plot(contrafactual_x, contrafactual_y, color=NARANJA, linewidth=1.8,
             linestyle="--", marker="o", markersize=4, zorder=3)
ejes[0].set_xticks(anios)
ejes[0].set_ylim(5.5, 33.0)
ejes[0].text(0.03, 0.60, "región tratada", transform=ejes[0].transAxes,
             color=AZUL, fontsize=9.5)
ejes[0].text(0.03, 0.22, "región control", transform=ejes[0].transAxes,
             color=VERDE, fontsize=9.5)
ejes[0].text(0.51, 0.97, "la reforma entra en vigor", transform=ejes[0].transAxes,
             color=REJILLA, fontsize=8.5, va="top")
anotar(ejes[0], "sin programa habría seguido\nen paralelo al control",
       xy=(0.5, 20.8), xytext=(0.10, 0.36), color=NARANJA)
ejes[0].annotate("", xy=(2.06, 26.9), xytext=(2.06, 22.9),
                 arrowprops=dict(arrowstyle="<->", color=ROJO, linewidth=1.6))
anotar(ejes[0], "la brecha que queda\nes el efecto: 4,0 puntos",
       xy=(2.06, 24.9), xytext=(0.42, 0.72), color=ROJO, flecha=False)
titulo(ejes[0], "El efecto es la brecha que queda",
       "los niveles ya diferían antes: DiD compara los cambios, no los niveles")
ejes[0].set_xlabel("años respecto a la reforma")
ejes[0].set_ylabel("empleo (%)")
numeros(ejes[0])
rejilla(ejes[0])

# --- Panel 2: regresion discontinua ---------------------------------------------------
notas = azar.uniform(6.0, 8.0, 320)
media_curso = (48.0 + 7.0 * (notas - 7.0)
               + np.where(notas >= 7.0, 3.5, 0.0)
               + azar.normal(0, 1.7, notas.size))

izquierda = notas < 7.0
recta_izq = np.polyfit(notas[izquierda], media_curso[izquierda], 1)
recta_der = np.polyfit(notas[~izquierda], media_curso[~izquierda], 1)
tramo_izq = np.linspace(6.0, 7.0, 40)
tramo_der = np.linspace(7.0, 8.0, 40)

ejes[1].scatter(notas, media_curso, s=13, color=AZUL, alpha=0.35,
                edgecolors="none", zorder=2)
ejes[1].plot(tramo_izq, np.polyval(recta_izq, tramo_izq), color=MORADO,
             linewidth=1.8, zorder=3)
ejes[1].plot(tramo_der, np.polyval(recta_der, tramo_der), color=MORADO,
             linewidth=1.8, zorder=3)
ejes[1].axvline(7.0, color=REJILLA, linewidth=1.2, linestyle="--", zorder=1)

salto_abajo = float(np.polyval(recta_izq, 7.0))
salto_arriba = float(np.polyval(recta_der, 7.0))
ejes[1].annotate("", xy=(7.06, salto_arriba), xytext=(7.06, salto_abajo),
                 arrowprops=dict(arrowstyle="<->", color=ROJO, linewidth=1.6))
ejes[1].text(7.12, (salto_abajo + salto_arriba) / 2.0,
             "3,5 puntos\n(el efecto de la beca)", color=ROJO, fontsize=9, va="center")
ejes[1].text(0.03, 0.97, "el corte: beca a partir del 7,00", transform=ejes[1].transAxes,
             color=REJILLA, fontsize=8.5, va="top")
anotar(ejes[1], "justo a cada lado del corte\nlos alumnos son casi idénticos",
       xy=(6.35, 44.0), xytext=(0.03, 0.72), color=TEXTO)
titulo(ejes[1], "El salto justo en el corte",
       "la nube es continua salvo en el 7,00: eso es lo que se atribuye a la beca")
ejes[1].set_xlabel("nota de acceso")
ejes[1].set_ylabel("nota media del segundo curso")
numeros(ejes[1])
rejilla(ejes[1])

guardar(fig, "did-y-discontinuidad")
