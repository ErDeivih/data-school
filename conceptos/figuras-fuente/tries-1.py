"""tries-1.py — el árbol de prefijos dibujado con las cinco palabras del ejemplo y lo que
cuesta una consulta por prefijo frente a recorrer una tabla hash. Página de tries (fase 10)."""

import numpy as np

from comun import *

estilo()

# Las cinco palabras del ejemplo de la página, insertadas en este orden.
palabras = ["sol", "solo", "solar", "sal", "sarten"]

# --- El trie, nodo a nodo. Cada nodo lleva el carácter que representa y el conjunto de los
# que son fin de palabra. Son 13 nodos, los mismos que cuenta la página.
pos = {
    "raiz": (0.32, 0.74), "s": (0.32, 0.64),
    "o": (0.18, 0.53), "a": (0.56, 0.53),
    "sol_l": (0.14, 0.42), "solo_o": (0.05, 0.30), "solar_a": (0.25, 0.30), "solar_r": (0.25, 0.19),
    "sal_l": (0.47, 0.42), "sar_r": (0.67, 0.42), "sar_t": (0.67, 0.32),
    "sar_e": (0.67, 0.22), "sar_n": (0.67, 0.12),
}
aristas = [("raiz", "s"), ("s", "o"), ("s", "a"), ("o", "sol_l"), ("sol_l", "solo_o"),
           ("sol_l", "solar_a"), ("solar_a", "solar_r"), ("a", "sal_l"), ("a", "sar_r"),
           ("sar_r", "sar_t"), ("sar_t", "sar_e"), ("sar_e", "sar_n")]
fin = {"sol_l", "solo_o", "solar_r", "sal_l", "sar_n"}    # fin de palabra
caracter = {"s": "s", "o": "o", "a": "a", "sol_l": "l", "solo_o": "o", "solar_a": "a",
            "solar_r": "r", "sal_l": "l", "sar_r": "r", "sar_t": "t", "sar_e": "e", "sar_n": "n"}

ALTO = 0.8          # el eje y mide 0,8 para que un paso en x mida lo mismo en pantalla que en y


def frac(x, y):
    """Pasa coordenadas del dibujo (cuadradas) a fracción de eje, que es lo que usa anotar()."""
    return (x, y / ALTO)


fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.7))

# --- Izquierda: el trie. Los nodos con aro rojo son fin de palabra; los demás, solo prefijos
# que alguien continúa.
lienzo = ejes[0]
for a, b in aristas:
    lienzo.annotate("", xy=pos[b], xytext=pos[a], zorder=1,
                    arrowprops=dict(arrowstyle="-", shrinkA=15, shrinkB=15, color=TEXTO,
                                    linewidth=1.5))
for nombre, (x, y) in pos.items():
    es_fin = nombre in fin
    lienzo.scatter(x, y, s=620, facecolor="none", edgecolor=ROJO if es_fin else REJILLA,
                   linewidth=2.8 if es_fin else 1.6, zorder=4)
    lienzo.text(x, y, caracter.get(nombre, ""), ha="center", va="center", fontsize=9.5,
                color=TEXTO, zorder=5)
lienzo.text(0.26, 0.74, "raíz", ha="right", va="center", fontsize=9, color=TEXTO)
anotar(lienzo, "s-o-l se guarda una sola vez\ny sirve para «sol», «solo» y «solar»",
       xy=pos["sol_l"], xytext=frac(0.02, 0.06), color=AZUL, flecha=False)
anotar(lienzo, "el nodo de «sol» está marcado como fin y además\ntiene hijos: es palabra y prefijo a la vez",
       xy=pos["sol_l"], xytext=frac(0.99, 0.76), color=ROJO, flecha=False, align="right")
lienzo.set_xlim(0, 1)
lienzo.set_ylim(0, ALTO)
lienzo.axis("off")                             # es un diagrama: ni ejes ni rejilla
titulo(lienzo, "13 nodos para cinco palabras",
       "cada nodo es un prefijo; el aro rojo marca dónde termina una palabra almacenada")

# --- Derecha: lo que cuesta saber si existe alguna palabra que empiece por «sol». El trie
# baja 3 caracteres; la tabla hash tiene que mirar clave por clave.
n_palabras = np.logspace(1, 6, 200)
pasos_trie = np.full(n_palabras.shape, 3.0)               # los caracteres de «sol»
pasos_hash = n_palabras                                   # al menos una comprobación por clave
ejes[1].loglog(n_palabras, pasos_hash, color=ROJO, linewidth=2.0,
               label="tabla hash: una comprobación por clave")
ejes[1].loglog(n_palabras, pasos_trie, color=AZUL, linewidth=2.4,
               label="trie: los 3 caracteres de «sol»")
anotar(ejes[1], "con un millón de palabras, la tabla mira\nun millón de claves; el trie, tres",
       xy=(1e6, 1e6), xytext=(0.04, 0.86), color=ROJO)
anotar(ejes[1], "el trie no depende de cuántas palabras\nhaya: baja 3 caracteres y mira el subárbol",
       xy=(1e3, 3), xytext=(0.04, 0.70), color=AZUL, flecha=False)
titulo(ejes[1], "Buscar por prefijo: 3 pasos frente a n claves",
       "¿hay alguna palabra que empiece por «sol»?, en escala logarítmica")
ejes[1].set_xlabel("palabras almacenadas")
ejes[1].set_ylabel("comprobaciones por consulta")
ejes[1].set_ylim(1.5, 1e7)
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="both")

guardar(fig, "tries-prefijos-y-consulta")
