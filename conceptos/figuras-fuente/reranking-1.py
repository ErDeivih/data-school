"""reranking-1.py — lo que hace una segunda pasada sobre los candidatos: el documento bueno
sube puestos sin tocar el índice, y el precio es un tiempo que crece con el número de
candidatos. Figura de la pagina de reordenación (fase 8)."""

import numpy as np

from comun import *

estilo()

CONSULTA = "cambiar la contrasena de acceso"
# (documento, puntuacion de la etapa 1, relevancia real, texto)
CANDIDATOS = [
    ("A", 0.81, 2, "cambiar la contrasena de la cuenta"),
    ("B", 0.79, 1, "donde veo mi contrasena guardada"),
    ("C", 0.74, 3, "acceso a la cuenta y cambio de contrasena"),
    ("D", 0.72, 0, "recuperar la contrasena olvidada del correo"),
    ("E", 0.70, 2, "acceso desde el movil y datos personales"),
]


def pares(secuencia, n):
    return set(tuple(secuencia[i:i + n]) for i in range(len(secuencia) - n + 1))


def codificador_cruzado(q, doc):
    p = doc.split()
    return (sum(p.count(w) for w in q.split())
            + 2 * len(pares(q.split(), 2) & pares(p, 2))
            + 3 * len(pares(q.split(), 3) & pares(p, 3)))


etapa1 = [i for i, _, _, _ in sorted(CANDIDATOS, key=lambda c: -c[1])]
puntuaciones = {i: codificador_cruzado(CONSULTA, t) for i, _, _, t in CANDIDATOS}
etapa2 = sorted(puntuaciones, key=lambda i: -puntuaciones[i])

# Coste: la recuperacion es constante con el numero de candidatos y la reordenacion no.
candidatos = np.array([10, 25, 50, 100, 200, 500])
ms_por_pareja = 0.5
ms_recuperacion = 25.0

# Dos filas: el panel de los puestos necesita el ancho entero para que quepan el titulo,
# las etiquetas de cada lado y la leyenda sin pisarse.
fig, (arriba, abajo) = plt.subplots(2, 1, figsize=(10.4, 8.4))
fig.set_constrained_layout_pads(h_pad=0.09)   # aire entre los dos paneles

# --- Panel de arriba: cada candidato va del puesto que le da la etapa 1 al de la etapa 2 ---
for documento, _, relevancia, _ in CANDIDATOS:
    x0, x1 = etapa1.index(documento), etapa2.index(documento)
    if relevancia == 3:
        color, grosor, tamano = ROJO, 2.4, 9      # el unico que responde de verdad
    elif relevancia == 0:
        color, grosor, tamano = NARANJA, 2.0, 9   # el que no responde nada y sube
    else:
        color, grosor, tamano = AZUL, 1.2, 5
    arriba.plot([0, 1], [x0, x1], color=color, linewidth=grosor, marker="o",
                markersize=tamano, alpha=0.9)
    arriba.annotate(documento, (0, x0), textcoords="offset points", xytext=(-16, -3),
                    color=color, fontsize=10)
    arriba.annotate(documento, (1, x1), textcoords="offset points", xytext=(10, -3),
                    color=color, fontsize=10)
arriba.set_xlim(-0.35, 1.35)
arriba.set_ylim(5.3, -0.6)
arriba.set_xticks([0, 1])
arriba.set_yticks(range(5))
titulo(arriba, "Reordenar sube al bueno y también al malo")
arriba.set_ylabel("puesto en la lista (1 = primero)")
rejilla(arriba, "y")
numeros(arriba, "x")
arriba.set_xticklabels(["etapa 1\n(bi-codificador)", "etapa 2\n(codificador cruzado)"])
# La leyenda va debajo de las etiquetas del eje: dentro del panel taparía las líneas.
arriba.legend(handles=[plt.Line2D([], [], color=ROJO, linewidth=2.4, label="C: responde"),
                       plt.Line2D([], [], color=NARANJA, linewidth=2.0,
                                  label="D: no responde"),
                       plt.Line2D([], [], color=AZUL, linewidth=1.2, label="los demás")],
              loc="upper center", ncols=3, bbox_to_anchor=(0.5, -0.16), fontsize=9)

# --- Panel de abajo: el tiempo de la segunda pasada, lineal en el numero de candidatos ---
tiempos = ms_recuperacion + candidatos * ms_por_pareja
abajo.plot(candidatos, tiempos, color=ROJO, linewidth=1.9)
abajo.axhline(ms_recuperacion, color=CIAN, linewidth=1.4, linestyle="--")
# La recta sube de izquierda a derecha, así que el texto se coloca por encima de la recta
# (a la derecha) o por debajo de ella (a la izquierda), nunca encima.
anotar(abajo, "la recuperación no depende de m", xy=(450, ms_recuperacion),
       xytext=(0.03, 0.10), color=CIAN)
anotar(abajo, f"200 candidatos: {tiempos[-1]:.0f} ms", xy=(200, tiempos[-1]),
       xytext=(0.28, 0.86), color=MORADO)
anotar(abajo, f"50 candidatos: {ms_recuperacion + 50 * ms_por_pareja:.0f} ms",
       xy=(50, ms_recuperacion + 50 * ms_por_pareja), xytext=(0.28, 0.78), color=MORADO)
titulo(abajo, "Cada candidato extra se paga en milisegundos")
abajo.set_xlabel("candidatos que pasan al reordenador (m)")
abajo.set_ylabel("milisegundos por consulta")
rejilla(abajo)
numeros(abajo)

guardar(fig, "reranking-puestos-y-coste")
