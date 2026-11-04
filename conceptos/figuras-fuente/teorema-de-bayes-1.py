"""teorema-de-bayes-1.py — de donde sale el 15 % de un test con 90 % de acierto.

Izquierda: los 585 positivos que produce una población de 10.000 personas, separados en
verdaderos (enfermos) y falsos (sanos). Los falsos son cinco veces más numerosos, y eso fija
el posterior. Derecha: que pasa con ese posterior cuando se repite un test independiente.
"""

import numpy as np

from comun import *

estilo()

prevalencia = 0.01        # P(enfermo)
sensibilidad = 0.90       # P(positivo | enfermo)
especificidad = 0.95      # P(negativo | sano)

# Poblacion concreta de 10.000 personas: es la cuenta que se hace a mano en la pagina.
total = 10000
enfermos = total * prevalencia
sanos = total - enfermos
vp = enfermos * sensibilidad              # 90
fn = enfermos * (1 - sensibilidad)        # 10
fp = sanos * (1 - especificidad)          # 495
vn = sanos * especificidad                # 9405
assert abs((vp + fn) - enfermos) < 1e-9 and abs((fp + vn) - sanos) < 1e-9
assert abs(vp + fp - 585) < 1e-9

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.5))

# --- Panel izquierdo: composicion de los positivos -------------------------------
alturas = [vp, fp]
bases = [0, vp]
colores = [AZUL, ROJO]
izq.bar([0, 0], alturas, bottom=bases, width=0.5, color=colores)
for base, alto, color in zip(bases, alturas, colores):
    izq.vlines(0.26, base, base + alto, color=TEXTO, linewidth=0.8)
    izq.text(0.30, base + alto / 2, f"{alto:.0f}", color=color, fontsize=11,
             fontweight="bold", va="center", ha="left")

izq.text(0, vp / 2, "90", color="white", fontsize=10, ha="center", va="center")
izq.text(0, vp + fp / 2, "495", color="white", fontsize=10, ha="center", va="center")

posterior = vp / (vp + fp)
izq.annotate(
    "de cada 585 positivos\nsolo 90 estan enfermos\nP(enfermo | positivo) = 15,4 %",
    xy=(0.0, vp), xytext=(0.72, 300), color=TEXTO, fontsize=9.5,
    arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=1.0),
)
izq.set_xticks([])
izq.set_xlim(-0.45, 1.9)
izq.set_ylim(0, 780)
izq.set_ylabel("personas")
izq.set_title("La mayoria de los positivos son sanos")
numeros(izq)
rejilla(izq)

# --- Panel derecho: repetir el test con un resultado independiente ---------------
p = prevalencia
pasos = [p]
for _ in range(4):
    p = sensibilidad * p / (sensibilidad * p + (1 - especificidad) * (1 - p))
    pasos.append(p)
pasos = np.array(pasos)
assert abs(pasos[1] - 0.1538) < 0.001 and abs(pasos[3] - 0.9833) < 0.001

x = np.arange(5)
der.plot(x, pasos, color=MORADO, linewidth=1.8, marker="o", markersize=5)
der.axhline(0.5, color=REJILLA, linewidth=0.9, linestyle=":")
for xi, yi in zip(x, pasos):
    der.annotate(f"{yi:.1%}".replace(".", ","), xy=(xi, yi), xytext=(0, 9),
                 textcoords="offset points", color=MORADO, fontsize=9,
                 ha="left" if xi < 4 else "right")
der.set_xticks(x)
der.set_xticklabels(["previa", "1 test", "2 tests", "3 tests", "4 tests"])
der.set_ylim(0, 1.14)
der.set_ylabel("P(enfermo | positivos)")
der.set_title("Tres tests para pasar del 90 %")
der.text(0.06, 0.58, "la linea punteada es el 50 %", color=REJILLA, fontsize=8.5)
numeros(der, ejes="y")
rejilla(der)

guardar(fig, "bayes-positivos-y-repetición")
