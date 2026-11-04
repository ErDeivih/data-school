"""recursion-y-backtracking-1.py — lo que cuesta llamarse a uno mismo y lo que ahorra podar.
La figura de la página de recursión y backtracking (fase 10).

Izquierda: número de llamadas de Fibonacci, contadas de verdad, con y sin memoria. La recursión
ingenua crece como φⁿ (una llamada más por cada nivel), la memoizada es lineal: 2n − 1 llamadas.
Derecha: nodos que explora el backtracking de las n reinas frente a las nⁿ hojas del árbol de
decisiones completo. La poda reduce, pero la curva sigue siendo exponencial.
"""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)          # semilla fija: las cuentas salen siempre igual

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.4))

# --- Izquierda: llamadas de Fibonacci, contadas y no estimadas ------------------------
def fib_llamadas(n, contador):
    """La recursión ingenua de la página, contando cada llamada."""
    contador[0] += 1
    if n < 2:
        return n
    return fib_llamadas(n - 1, contador) + fib_llamadas(n - 2, contador)


# El número exacto de llamadas de la versión ingenua es 2 · F(n+1) − 1, con F la sucesión
# de Fibonacci. Se comprueba contra la cuenta real en los tamaños pequeños y se usa la
# fórmula a partir de ahí: contar 2,7 millones de llamadas para dibujar no aporta nada.
F = [0, 1]
for _ in range(40):
    F.append(F[-1] + F[-2])

valores_n = np.arange(5, 31)
ingenua = []
for n in valores_n:
    if n <= 18:                          # se cuenta de verdad hasta donde es barato
        contador = [0]
        fib_llamadas(int(n), contador)
        assert contador[0] == 2 * F[n + 1] - 1, "la fórmula no coincide con la cuenta real"
        ingenua.append(contador[0])
    else:
        ingenua.append(2 * F[n + 1] - 1)
ingenua = np.array(ingenua, dtype=float)
memoizada = 2 * valores_n - 1            # cada valor genera una llamada que calcula y otra que consulta

ax = ejes[0]
ax.semilogy(valores_n, ingenua, color=ROJO, linewidth=1.9, marker="o", markersize=3.5,
            label="recursión ingenua: llamadas = 2 · F(n+1) − 1")
ax.semilogy(valores_n, memoizada, color=AZUL, linewidth=1.9, marker="s", markersize=3.5,
            label="con memoria: llamadas = 2n − 1")
anotar(ax, "fib(30) hace 2.692.537 llamadas\npara devolver 832.040",
       xy=(30, float(ingenua[-1])), xytext=(0.05, 0.60), color=ROJO)
anotar(ax, "los mismos 832.040 con 59 llamadas:\nun 99,998 % menos",
       xy=(30, float(memoizada[-1])), xytext=(0.97, 0.28), color=AZUL, align="right")
titulo(ax, "Guardar el resultado corta la exponencial",
       "llamadas de Fibonacci con n de 5 a 30, en escala logarítmica")
ax.set_xlabel("n: tamaño del problema")
ax.set_ylabel("número de llamadas")
ax.set_ylim(5, 2e7)
ax.legend(loc="upper left")
rejilla(ax)
numeros(ax)


# --- Derecha: lo que ahorra la poda en las n reinas -----------------------------------
def nodos_reinas(n):
    """Nodos del árbol que explora el backtracking con poda de columna y diagonal."""
    nodos = 0

    def explorar(fila, colocadas):
        nonlocal nodos
        nodos += 1
        if fila == n:
            return
        for col in range(n):
            if all(c != col and abs(f - fila) != abs(c - col) for f, c in colocadas):
                colocadas.append((fila, col))
                explorar(fila + 1, colocadas)
                colocadas.pop()
    explorar(0, [])
    return nodos


reinas = np.arange(4, 11)
explorados = np.array([nodos_reinas(int(n)) for n in reinas], dtype=float)
sin_poda = reinas.astype(float) ** reinas               # el árbol completo tiene nⁿ hojas
ancho = 0.38

ax = ejes[1]
ax.bar(reinas - ancho / 2, sin_poda, width=ancho, color=ROJO, alpha=0.85,
       label="árbol completo sin poda: nⁿ hojas")
ax.bar(reinas + ancho / 2, explorados, width=ancho, color=AZUL, alpha=0.9,
       label="nodos que explora el backtracking")
ax.set_yscale("log")
ax.set_ylim(5, 1e12)
for n, e in zip(reinas, explorados):
    ax.text(n + ancho * 1.05, e, f"{int(e):,}".replace(",", "."), fontsize=7.5,
            color=AZUL, ha="left", va="center", zorder=5)
anotar(ax, "con 8 reinas: 2.057 nodos frente a\nlas 16.777.216 hojas del árbol completo",
       xy=(8, float(explorados[4])), xytext=(0.03, 0.72), color=AZUL)
anotar(ax, "la poda no quita la exponencial:\nsolo la retrasa unos tableros",
       xy=(10, float(explorados[-1])), xytext=(0.02, 0.56), color=ROJO, flecha=False)
titulo(ax, "Podar recorta el árbol, no lo aplana",
       "nodos explorados por el backtracking frente a las hojas del árbol completo")
ax.set_xlabel("tamaño del tablero: n reinas en n × n")
ax.set_ylabel("nodos (escala logarítmica)")
ax.set_xticks(reinas)
ax.set_xlim(3.4, 11.9)
ax.legend(loc="upper left")
rejilla(ax)
numeros(ax, ejes="x")

guardar(fig, "recursion-llamadas-y-poda")
