"""alucinaciones-y-limites-1.py — las tres comprobaciones baratas contra las alucinaciones:
el anclaje de los números, la fidelidad afirmación a afirmación y la consistencia al
reformular. Figura de la pagina de alucinaciones y limites (fase 8)."""

import numpy as np

from comun import *

estilo()

CONTEXTO = ("Las devoluciones se admiten dentro de los 14 dias naturales desde la entrega. "
            "Para productos personalizados el plazo es de 7 dias. El reembolso se emite "
            "en un máximo de 5 dias laborables tras la recepción.")
EN_CONTEXTO = {"14", "7", "5"}

# Las tres respuestas del ejemplo, con los numeros que usa cada una.
RESPUESTAS = [
    ("1. «14 días naturales desde la entrega»", ["14"], "responde"),
    ("2. «30 días según la normativa europea»", ["30"], "inventa el número y la norma"),
    ("3. «14 días, o 10 si es personalizado»", ["14", "10"], "mezcla: el 14 sí, el 10 no"),
]
ETIQUETA_RESPUESTA = ["respuesta 1\n(todo anclado)", "respuesta 2\n(nada anclado)",
                      "respuesta 3\n(la trampa fina)"]

# Consistencia: la misma pregunta formulada de cuatro maneras.
VARIANTES = ["directa", "con contexto", "reformulada", "con presión"]
PLAZOS = [14, 14, 14, 30]

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.0),
                         gridspec_kw={"width_ratios": [1.15, 1.0]})

# Panel izquierdo: cada respuesta descompuesta numero a numero
y = np.arange(len(RESPUESTAS))
altura = 0.5
for indice, (_, cifras, _) in enumerate(RESPUESTAS):
    for posicion, cifra in enumerate(cifras):
        anclado = cifra in EN_CONTEXTO
        color = VERDE if anclado else ROJO
        ejes[0].barh(y[indice], 1, left=posicion, height=altura, color=color)
        ejes[0].annotate(cifra, (posicion + 0.5, y[indice]), ha="center", va="center",
                         color="white", fontsize=10)
        # el numero que no esta en el contexto se marca con un circulo alrededor
        if not anclado:
            ejes[0].plot([posicion + 0.5], [y[indice]], "o", markersize=26,
                         markerfacecolor="none", markeredgecolor=TEXTO,
                         markeredgewidth=1.2)
for indice, (texto, _, _) in enumerate(RESPUESTAS):
    ejes[0].annotate(texto, (0, y[indice] - 0.42), textcoords="offset points",
                     xytext=(0, -1), color=TEXTO, fontsize=8.5, va="top")
# Un texto por respuesta, con el anclaje medido (numeros del contexto / numeros usados)
for indice, (_, cifras, _) in enumerate(RESPUESTAS):
    anclados = sum(n in EN_CONTEXTO for n in cifras)
    ejes[0].annotate(f"anclaje {anclados}/{len(cifras)}", (len(cifras) + 0.15, y[indice]),
                     va="center", color=TEXTO, fontsize=9)
ejes[0].set_xlim(0, 3.5)
ejes[0].set_ylim(len(RESPUESTAS) - 0.4, -0.95)
ejes[0].set_yticks(y)
ejes[0].set_yticklabels(ETIQUETA_RESPUESTA)
ejes[0].set_xticks(range(3))
ejes[0].set_xlabel("números que usa la respuesta")
titulo(ejes[0], "Basta un número inventado para perder el anclaje",
       "un solo número fuera del contexto desancla la respuesta")
rejilla(ejes[0], "x")
numeros(ejes[0], "x")
ejes[0].legend(handles=[plt.Rectangle((0, 0), 1, 1, color=VERDE),
                        plt.Rectangle((0, 0), 1, 1, color=ROJO)],
               labels=["está en el contexto", "no aparece en ninguna fuente"],
               loc="upper right", fontsize=8.5)

# Panel derecho: consistencia. El dato estable se repite; el que se sugiere en la pregunta
# aparece solo cuando el usuario lo insinua.
x = np.arange(len(VARIANTES))
tonos = [VERDE if p == 14 else ROJO for p in PLAZOS]
ejes[1].bar(x, PLAZOS, color=tonos, width=0.55)
for posicion, plazo in zip(x, PLAZOS):
    ejes[1].annotate(str(plazo), (posicion, plazo), textcoords="offset points",
                     xytext=(0, 4), ha="center", color=TEXTO, fontsize=10)
# Las dos lecturas del panel caben por encima de las barras verdes (que llegan a 14) y a la
# izquierda de la barra roja: el texto va en coordenadas del eje y no se pisa con ellas.
anotar(ejes[1], "el dato estable se repite", xy=(1, 14), xytext=(0.05, 0.52), color=VERDE)
anotar(ejes[1], "aquí el modelo confirma\nla cifra que le sugiere el usuario",
       xy=(x[-1], PLAZOS[-1]), xytext=(0.26, 0.90), color=ROJO)
ejes[1].set_xticks(x)
ejes[1].set_xticklabels([v.replace(" ", "\n") for v in VARIANTES])
ejes[1].set_xlim(-0.6, 3.6)
ejes[1].set_ylim(0, 39)
ejes[1].set_ylabel("plazo que responde, en días")
titulo(ejes[1], "Tres respuestas iguales y una que cambia",
       "reformular la pregunta no debería mover el plazo")
rejilla(ejes[1])
numeros(ejes[1], "y")

guardar(fig, "alucinaciones-anclaje-y-consistencia")
