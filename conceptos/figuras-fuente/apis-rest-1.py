"""apis-rest-1.py — las dos facturas de paginar: por desplazamiento la página profunda cuesta
más, y una inserción entre dos peticiones repite elementos. La figura de la página de APIs REST
(fase 11)."""

import numpy as np

from comun import *

estilo()

LIMITE = 100                        # pedidos por página, como en el ejemplo de la página
paginas = np.arange(1, 21)
# Modelo conservador: el motor recorre y descarta todo lo anterior al offset. Con un índice que
# resuelva el salto es más barato, pero el coste sigue creciendo con la profundidad.
filas_offset = paginas * LIMITE
filas_cursor = np.full_like(paginas, LIMITE)      # el cursor recuerda por dónde ibas

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.0))

# --- Izquierda: lo que cuesta servir una página --------------------------------------
izq.plot(paginas, filas_offset, color=ROJO, linewidth=1.8, marker="o", markersize=3,
         label="offset (desplazamiento)")
izq.plot(paginas, filas_cursor, color=VERDE, linewidth=1.8, marker="o", markersize=3,
         label="cursor")
izq.fill_between(paginas, filas_cursor, filas_offset, color=ROJO, alpha=0.10)
izq.set_ylim(0, filas_offset.max() * 1.18)
izq.annotate("filas que se leen y se tiran",
             xy=(13, 13 * LIMITE), xytext=(3.2, 1620), color=ROJO, fontsize=9,
             arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9))
izq.annotate("el cursor no crece",
             xy=(17, LIMITE), xytext=(9.5, 330), color=VERDE, fontsize=9,
             arrowprops=dict(arrowstyle="->", color=VERDE, linewidth=0.9))
# Titulo corto + explicacion en pequeño: los dos caben en los 409 px del panel.
titulo(izq, "Servir la página 20 cuesta 20 veces más",
       "2.000 filas leídas frente a las 100 que se devuelven")
izq.set_xlabel("número de página (100 pedidos por página)")
izq.set_ylabel("filas leídas para servir la página")
izq.legend(loc="upper left")
rejilla(izq)
numeros(izq)

# --- Derecha: una inserción descoloca las páginas -------------------------------------
L = 4
serie = np.arange(1, 13)                       # 12 pedidos, 4 por página
pagina1 = serie[:L]
pagina2 = serie[L:2 * L]
con_nuevo = np.concatenate(([99], serie))      # entra un pedido nuevo por delante
pagina2_tras = con_nuevo[L:2 * L]              # el offset no se entera de la inserción

filas = [
    ("página 1\n(las dos veces)", pagina1, set()),
    ("página 2\nsin inserciones", pagina2, set()),
    ("página 2\ntras insertar un pedido", pagina2_tras, set(pagina1)),
]
for y, (etiqueta, valores, repetidos) in enumerate(filas):
    for x, valor in enumerate(valores):
        repite = valor in repetidos
        color = ROJO if repite else (AZUL if y == 0 else VERDE)
        der.scatter(x, y, s=1200, marker="s", facecolor=color, edgecolor=color,
                    alpha=0.32 if repite else 0.14, linewidth=1.8 if repite else 0.8)
        der.text(x, y, str(valor), ha="center", va="center", fontsize=9, color=TEXTO,
                 fontweight="bold" if repite else "normal")
der.set_yticks([0, 1, 2], [f[0] for f in filas], fontsize=9)
der.set_ylim(-0.8, 2.8)
der.set_xlim(-0.75, L - 0.15)
der.invert_yaxis()                              # la página 1 arriba: el orden en que se lee
der.set_xticks([])
der.grid(False)
for lado in ("top", "right", "bottom", "left"):
    der.spines[lado].set_visible(False)
titulo(der, "Una inserción descoloca las páginas",
       "el id 4 viaja en la página 1 y otra vez en la 2")

guardar(fig, "apis-rest-coste-paginación")
