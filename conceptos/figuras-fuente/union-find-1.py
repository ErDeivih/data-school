"""union-find-1.py — lo que hace de verdad la compresión de caminos: aplana el árbol en la
primera consulta y deja las siguientes casi gratis. Página de union-find (fase 10)."""

import numpy as np

from comun import *

estilo()


class UnionFind:
    """Partición con unión por rango y compresión de caminos, contando los saltos de find()."""

    def __init__(self, n, comprimir=True):
        self.padre = list(range(n))
        self.rango = [0] * n
        self.comprimir = comprimir
        self.saltos = 0

    def find(self, x):
        raiz = x
        while self.padre[raiz] != raiz:        # primera pasada: llegar a la raíz
            raiz = self.padre[raiz]
            self.saltos += 1
        if self.comprimir:                     # segunda pasada: colgar del camino a la raíz
            while self.padre[x] != raiz:
                self.padre[x], x = raiz, self.padre[x]
        return raiz

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False                       # ya estaban juntos: no se toca nada
        if self.rango[rx] < self.rango[ry]:
            rx, ry = ry, rx                    # el árbol más bajo cuelga del más alto
        self.padre[ry] = rx
        if self.rango[rx] == self.rango[ry]:
            self.rango[rx] += 1
        return True


# --- El ejemplo de la página: 6 elementos, tres uniones y una consulta que comprime.
uf = UnionFind(6)
for a, b in ((0, 1), (2, 3), (1, 3)):
    uf.union(a, b)
padre_antes = list(uf.padre)
uf.find(3)
padre_despues = list(uf.padre)

# --- Cadena degenerada de 500 nodos: el peor caso para find(), consultado 200 veces.
CADENA, CONSULTAS = 500, 200
acumulado = {}
for comprimir in (False, True):
    u = UnionFind(CADENA, comprimir)
    for i in range(1, CADENA):
        u.padre[i] = i - 1                     # se salta la unión por rango a propósito
    u.rango = [0] * CADENA
    saltos = []
    for _ in range(CONSULTAS):
        u.find(CADENA - 1)                     # siempre el mismo extremo: el peor caso
        saltos.append(u.saltos)
    acumulado[comprimir] = np.array(saltos)

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.7))


def nodo(eje, p, texto, color=TEXTO):
    eje.scatter(*p, s=760, facecolor="none", edgecolor=color, linewidth=2.4, zorder=4)
    eje.text(p[0], p[1], texto, ha="center", va="center", fontsize=10.5, color=TEXTO, zorder=5)


def arista(eje, a, b, color=TEXTO, linea="-"):
    eje.annotate("", xy=b, xytext=a, zorder=1,
                 arrowprops=dict(arrowstyle="-", shrinkA=16, shrinkB=16, color=color,
                                 linewidth=2.2, linestyle=linea))


# --- Izquierda: el conjunto {0, 1, 2, 3} antes y después de find(3). A la izquierda, el
# camino 3 → 2 → 0; a la derecha, los tres nodos colgando ya de la raíz.
ALTO = 0.8          # el eje y mide 0,8 para que un paso en x mida lo mismo en pantalla que en y


def frac(x, y):
    """Pasa coordenadas del dibujo (cuadradas) a fracción de eje, que es lo que usa anotar()."""
    return (x, y / ALTO)


lienzo = ejes[0]
antes = {0: (0.20, 0.50), 1: (0.06, 0.34), 2: (0.34, 0.34), 3: (0.34, 0.20)}
despues = {0: (0.72, 0.50), 1: (0.56, 0.32), 2: (0.72, 0.28), 3: (0.88, 0.32)}
arista(lienzo, antes[0], antes[1])
arista(lienzo, antes[0], antes[2])
arista(lienzo, antes[2], antes[3], color=ROJO, linea="--")
arista(lienzo, despues[0], despues[1])
arista(lienzo, despues[0], despues[2])
arista(lienzo, despues[0], despues[3], color=ROJO)
for u in antes:
    nodo(lienzo, antes[u], str(u), color=ROJO if u == 3 else TEXTO)
    nodo(lienzo, despues[u], str(u), color=ROJO if u == 3 else TEXTO)
lienzo.text(0.02, 0.72, "antes de find(3)", fontsize=9, color=TEXTO)
lienzo.text(0.02, 0.64, "padre = " + str(padre_antes), fontsize=8.5, color=REJILLA)
lienzo.text(0.52, 0.72, "después de find(3)", fontsize=9, color=TEXTO)
lienzo.text(0.52, 0.64, "padre = " + str(padre_despues), fontsize=8.5, color=REJILLA)
anotar(lienzo, "3 → 2 → 0: dos saltos", xy=antes[3], xytext=frac(0.02, 0.10), color=ROJO)
anotar(lienzo, "tras comprimir, el 3 cuelga de la raíz", xy=despues[3],
       xytext=frac(0.02, 0.03), color=ROJO, flecha=False)
anotar(lienzo, "el 4 y el 5 quedan fuera: son raíces\nde sus propios conjuntos",
       xy=despues[3], xytext=frac(0.99, 0.12), color=TEXTO, flecha=False, align="right")
lienzo.set_xlim(0, 1)
lienzo.set_ylim(0, ALTO)
lienzo.axis("off")                             # es un diagrama: ni ejes ni rejilla
titulo(lienzo, "find(3) aplana el camino 3 → 2 → 0",
       "el conjunto {0, 1, 2, 3} antes y después de esa consulta, con compresión en dos pasadas")

# --- Derecha: saltos acumulados de 200 consultas al mismo nodo, con y sin compresión.
consultas = np.arange(1, CONSULTAS + 1)
ejes[1].semilogy(consultas, acumulado[False], color=ROJO, linewidth=2.0,
                 label="sin compresión: 499 saltos por consulta")
ejes[1].semilogy(consultas, acumulado[True], color=AZUL, linewidth=2.0,
                 label="con compresión: 499 la primera y 1 las demás")
anotar(ejes[1], f"200 consultas sin comprimir suman\n{acumulado[False][-1]:,} saltos".replace(",", "."),
       xy=(175, acumulado[False][-25]), xytext=(0.04, 0.88), color=ROJO)
anotar(ejes[1], f"comprimiendo suman {acumulado[True][-1]}: la primera\nconsulta paga la cadena y aplana el árbol",
       xy=(60, acumulado[True][-1]), xytext=(0.16, 0.38), color=AZUL)
titulo(ejes[1], "Sin compresión, cada consulta paga la cadena entera",
       "consultas repetidas de find(499) sobre una cadena degenerada de 500 nodos")
ejes[1].set_xlabel("consultas de find(499)")
ejes[1].set_ylabel("saltos acumulados")
ejes[1].set_ylim(300, 3e5)
ejes[1].legend(loc="lower right", fontsize=8)
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="x")

guardar(fig, "union-find-compresion-y-saltos")
