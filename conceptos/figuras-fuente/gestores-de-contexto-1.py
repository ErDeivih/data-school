"""gestores-de-contexto-1.py — el orden en que entran y salen los bloques with, y que decide
el valor que devuelve __exit__. La figura de la pagina de gestores de contexto (fase 3)."""

import numpy as np
from matplotlib.colors import to_rgb

from comun import *

estilo()

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.2))

# --- Izquierda: tres bloques anidados, entran hacia dentro y salen hacia fuera -------
# Escalera de profundidad: la altura es el numero de bloques abiertos en cada momento.
xs = [0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 4.0, 4.0, 5.0, 5.0, 6.0, 6.0, 6.4]
ys = [0.0, 0.0, 1.0, 1.0, 2.0, 2.0, 3.0, 3.0, 2.0, 2.0, 1.0, 1.0, 0.0, 0.0]
izq.plot(xs, ys, color=AZUL, linewidth=2.2, zorder=3)

# Aqui revienta el cuerpo: la salida ocurre igual, y en orden inverso.
izq.axvline(3.5, color=ROJO, linewidth=1.2, linestyle="--", zorder=2)
anotar(izq, "aquí revienta el cuerpo", xy=(3.5, 3.0), xytext=(0.02, 0.97), color=ROJO)

# Entradas: debajo de cada meseta, que es donde no hay linea.
izq.text(1.5, 0.62, "1º entra abrir fichero", ha="center", fontsize=8.5, color=AZUL)
izq.text(2.5, 1.62, "2º entra leer cabecera", ha="center", fontsize=8.5, color=AZUL)
izq.text(3.35, 2.62, "3º entra validar filas", ha="right", fontsize=8.5, color=AZUL)
# Salidas: numeradas al reves, que es justo lo que enseña la escalera.
izq.text(4.12, 2.82, "3º sale", fontsize=8.5, color=NARANJA)
izq.text(5.12, 1.82, "2º sale", fontsize=8.5, color=NARANJA)
izq.text(6.12, 0.82, "1º sale", fontsize=8.5, color=NARANJA)

izq.set_xlim(-0.1, 7.2)
izq.set_ylim(-0.45, 3.7)
izq.set_yticks([0, 1, 2, 3])
izq.set_xticks([])
izq.set_ylabel("bloques with abiertos")
izq.set_xlabel("tiempo")
titulo(izq, "El último que entra es el primero que sale",
       "tres bloques anidados: la salida va en orden inverso")

# --- Derecha: el valor que devuelve __exit__ decide el destino de la excepcion -------
filas = ["el cuerpo va bien", "el cuerpo lanza\nuna excepción"]
columnas = ["__exit__ devuelve\nNone o False", "__exit__ devuelve\nTrue"]
textos = [
    ["el recurso se suelta,\ntodo sigue igual", "el recurso se suelta:\nel valor da igual"],
    ["el recurso se suelta\ny la excepción sigue", "el recurso se suelta y la\nexcepción desaparece"],
]

colores = np.zeros((2, 2, 3))
for f in range(2):
    for c in range(2):
        # El unico cuadro peligroso es el de abajo a la derecha: se traga el error.
        colores[f, c] = to_rgb(ROJO) if (f == 1 and c == 1) else (
            to_rgb(VERDE) if f == 0 else to_rgb(NARANJA))
der.imshow(colores, origin="upper", aspect="auto")
for f in range(2):
    for c in range(2):
        der.text(c, f, textos[f][c], ha="center", va="center", fontsize=8,
                 color="white" if (f == 0 or c == 1) else TEXTO)
der.set_xticks([0, 1])
der.set_xticklabels(columnas, fontsize=8.5)
der.set_yticks([0, 1])
der.set_yticklabels(filas, fontsize=8.5)
der.set_xlabel("lo que devuelve el gestor")
titulo(der, "Qué decide el valor que devuelve __exit__",
       "devolver True absorbe el error en silencio")
# La rejilla la dibujan los bordes de las celdas de imshow: no hace falta rejilla() aqui.

guardar(fig, "gestores-contexto-orden-de-salida")
