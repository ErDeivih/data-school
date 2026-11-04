"""privacidad-y-datos-en-llms-1.py — cuánto texto con identificadores sale de casa y a qué
precio. La figura de la página de privacidad de datos en LLMs (fase 8)."""

from comun import *

estilo()

TICKETS_DIA = 1000
DIAS = 30
PRECIO_MILLON = 1.0                     # dólares por millón de tokens de entrada

# Los tres diseños de la página: tokens por ticket y si lo que viaja lleva identificadores.
DISENOS = [
    ("A: el ticket tal cual", 300, ROJO, "con nombre y correo"),
    ("B: minimizado antes de enviar", 120, VERDE, "seudónimo, sin identificadores directos"),
    ("C: modelo local", 0, AZUL, "no sale nada de casa: 0 tokens"),
]
millones = [TICKETS_DIA * DIAS * tokens / 1e6 for _, tokens, _, _ in DISENOS]
CORTOS = ["A: tal cual", "B: minimizado", "C: local"]

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.1))

# --- Izquierda: cuánta información cruza la frontera cada mes -----------------
# Altura de cada banda del eje (0-1), para centrar las notas en la fila que comentan.
alto_banda = 1.0 / len(DISENOS)
for i, ((etiqueta, _, color, nota), valor) in enumerate(zip(DISENOS, millones)):
    if valor:
        ejes[0].barh(i, valor, color=color, height=0.5)
        # Solo el número pegado a la barra: la unidad la dice ya el eje x.
        ejes[0].text(valor + 0.3, i, coma(valor), va="center", fontsize=9, color=TEXTO)

# Cada nota se centra en su propia banda, en coordenadas del eje (0-1): así no cae encima
# del nombre del caso (que vive fuera del eje) ni en la banda del caso siguiente. Centradas
# en 0,83 / 0,50 / 0,17 las tres quedaban algo por debajo del centro de su barra.
def centro_banda(i):
    return 1 - (i + 0.5) * alto_banda

anotar(ejes[0], DISENOS[0][3], xy=(millones[0], 0), xytext=(0.68, centro_banda(0)),
       color=ROJO, flecha=False)
anotar(ejes[0], DISENOS[1][3], xy=(millones[1], 1), xytext=(0.34, centro_banda(1)),
       color=VERDE, flecha=False)
anotar(ejes[0], DISENOS[2][3], xy=(0.0, 2), xytext=(0.07, centro_banda(2)),
       color=VERDE, flecha=False)

ejes[0].set_yticks(range(len(DISENOS)))
ejes[0].set_yticklabels([d[0] for d in DISENOS], fontsize=8.5)
ejes[0].invert_yaxis()
ejes[0].set_xlim(0, 16)
ejes[0].set_xticks([0, 2, 4, 6, 8, 10, 12, 14, 16])
ejes[0].set_xlabel("millones de tokens enviados al mes (1.000 tickets al día)")
titulo(ejes[0], "Lo que cruza la frontera cada mes")
rejilla(ejes[0], "x")
numeros(ejes[0], "x")

# --- Derecha: lo que cuesta el modelo, que no es todo el coste ----------------
coste = [m * PRECIO_MILLON for m in millones]
for i, ((etiqueta, _, color, _), valor) in enumerate(zip(DISENOS, coste)):
    ejes[1].bar(i, max(valor, 0.0), color=color, width=0.55)
    ejes[1].text(i, valor + 0.35, f"{valor:.1f}".replace(".", ",") + " $", ha="center",
                 fontsize=9, color=TEXTO)

# Los ticks van escritos a mano: con el eje automatico el «0,0 $» de la barra vacia caia a
# 0,35 por encima del margen inferior. Con la rejilla de dos en dos se lee igual y no hay
# tick pegado al borde.
ejes[1].set_xticks(range(len(DISENOS)))
ejes[1].set_xticklabels(CORTOS, fontsize=8.5)
ejes[1].set_ylim(0, 12)
ejes[1].set_yticks([0, 2, 4, 6, 8, 10, 12])
ejes[1].set_ylabel("dólares al mes de modelo")
titulo(ejes[1], "El coste del modelo baja, el resto no")
rejilla(ejes[1])
numeros(ejes[1], "y")

guardar(fig, "privacidad-y-datos-en-llms-lo-que-sale")
