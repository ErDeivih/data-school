"""structured-output-1.py — por qué una expresión regular parece aguantar más que el
validador y no es así. La figura de la página de salida estructurada (fase 8)."""

import json
import re

from comun import *

estilo()

# Las cinco variantes del mismo dato que discute la página: todas dicen 1250,0 EUR.
CRUDO = [
    '{"importe": 1250.0, "moneda": "EUR"}',
    '{"importe": 1250.0, "moneda": "EUR",}',
    'El resultado es {"importe": 1250.0, "moneda": "EUR"} y nada más.',
    "```json\n{\"importe\": 1250.0, \"moneda\": \"EUR\"}\n```",
    "Aqui lo tienes: {'importe': 1250.0, 'moneda': 'EUR'}",
]
ETIQUETAS = ["objeto limpio", "coma final", "texto alrededor", "valla de codigo", "comillas simples"]
PATRON = re.compile(r'"importe"\s*:\s*([0-9.]+)')


def json_directo(texto):
    """¿Es JSON válido tal cual llegó?"""
    try:
        json.loads(texto)
        return True
    except json.JSONDecodeError:
        return False


def json_sin_vallas(texto):
    """¿Es JSON válido después de quitar las vallas de código de los extremos?"""
    limpio = re.sub(r"^```(?:json)?\s*|\s*```$", "", texto.strip())
    try:
        json.loads(limpio)
        return True
    except json.JSONDecodeError:
        return False


def regex_importe(texto):
    """¿Encuentra el número en alguna parte, aunque sea texto y no un objeto?"""
    return PATRON.search(texto) is not None


ESTRATEGIAS = [
    ("json.loads\ndirecto", json_directo, AZUL),
    ("json.loads\ntras quitar vallas", json_sin_vallas, VERDE),
    ("regex del\nimporte", regex_importe, NARANJA),
]
CORTOS = ["json.loads\ndirecto", "sin vallas", "regex"]

# Dos filas: el mapa de calor necesita el ancho entero para que las tres columnas y sus
# etiquetas no queden apretadas contra el borde.
fig, (arriba, abajo) = plt.subplots(2, 1, figsize=(9.8, 8.6))
fig.set_constrained_layout_pads(h_pad=0.10)   # aire entre los dos paneles

# --- Panel de arriba: cuántas de las cinco variantes acepta cada estrategia ----
aciertos = [sum(f(t) for t in CRUDO) for _, f, _ in ESTRATEGIAS]
for i, ((_, _, color), n) in enumerate(zip(ESTRATEGIAS, aciertos)):
    arriba.bar(i, n, color=color, width=0.62)
    arriba.text(i, n + 0.14, f"{n} de 5", ha="center", fontsize=9, color=TEXTO)

arriba.set_xticks(range(len(ESTRATEGIAS)))
arriba.set_xticklabels([e[0] for e in ESTRATEGIAS], fontsize=9)
arriba.set_ylim(0, 5.8)
arriba.set_ylabel("variantes aceptadas")
# El título corto deja el matiz para la nota, que va en el hueco de arriba a la izquierda
# (la única barra alta es la de la derecha). La nota se sube hasta el borde del eje: a la
# altura de antes, la línea de la rejilla del 5 le pasaba por encima del texto.
titulo(arriba, "La regex acepta más variantes que el validador")
anotar(arriba, "pero devuelve texto:\nno comprueba la moneda ni los campos",
       xy=(0.15, 4.6), xytext=(0.03, 0.94), flecha=False)
rejilla(arriba)
numeros(arriba, "y")

# --- Panel de abajo: qué variante sobrevive a cada estrategia ------------------
for j, (_, f, _) in enumerate(ESTRATEGIAS):
    for i, texto in enumerate(CRUDO):
        color = VERDE if f(texto) else ROJO
        abajo.scatter(j, i, marker="s", s=520, color=color, zorder=3)

abajo.set_xticks(range(len(ESTRATEGIAS)))
abajo.set_xticklabels(CORTOS, fontsize=9)
abajo.set_yticks(range(len(CRUDO)))
abajo.set_yticklabels(ETIQUETAS, fontsize=9)
abajo.set_xlim(-0.6, len(ESTRATEGIAS) - 0.4)
abajo.set_ylim(-0.7, len(CRUDO) - 0.3)
abajo.invert_yaxis()
# La nota del color va en la esquina de abajo a la derecha, la única sin cuadros.
anotar(abajo, "verde: la acepta\nrojo: falla", xy=(2.4, 4.5),
       xytext=(0.62, 0.05), flecha=False)
titulo(abajo, "Ninguna aguanta las cinco variantes")
abajo.set_xlabel("la que más acepta es la que menos garantiza", labelpad=9)
rejilla(abajo, "x")

guardar(fig, "structured-output-validar-o-raspar")
