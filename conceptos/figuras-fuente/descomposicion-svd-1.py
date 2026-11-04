"""descomposicion-svd-1.py — valores singulares: cuánto pesa cada dirección y qué cuesta
tirar las pequeñas. Figura de la página de descomposición en valores singulares (fase 1)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# Matriz 60x40 construida a propósito: 4 direcciones fuertes y ruido por todas las demás.
m, n, r = 60, 40, 4
B = azar.normal(size=(m, r)) @ azar.normal(size=(r, n))
M = B + 0.005 * np.linalg.norm(B, 2) * azar.normal(size=(m, n))

U, s, Vt = np.linalg.svd(M, full_matrices=False)
norma_total = float(np.linalg.norm(M))
rango_real = int(np.linalg.matrix_rank(M))

fig, (izq, der) = plt.subplots(1, 2, figsize=(10.6, 4.4))

# --- Panel izquierdo: el espectro de valores singulares ---
indices = np.arange(1, len(s) + 1)
izq.semilogy(indices, s, color=AZUL, linewidth=1.8, marker="o", markersize=3.5)
izq.axvline(r + 0.5, color=ROJO, linewidth=1.2, linestyle="--")
anotar(izq, "los cuatro primeros son la señal", xy=(3.0, s[2]), xytext=(0.16, 0.90),
       color=AZUL)
anotar(izq, "a partir de aquí todo son valores\npequeños y parecidos entre sí: ruido",
       xy=(r + 4.0, s[r + 3]), xytext=(0.22, 0.24), color=ROJO)
titulo(izq, "El espectro: cuatro direcciones mandan",
       "los demás valores singulares son pequeños y parecidos: el ruido que metimos")
izq.set_xlabel("número de valor singular (ya ordenados)")
izq.set_ylabel("tamaño del valor singular (escala logarítmica)")
rejilla(izq)
numeros(izq)

# --- Panel derecho: qué se pierde al truncar ---
ks = np.arange(1, 13)
error = np.array([float(np.linalg.norm(M - U[:, :k] @ np.diag(s[:k]) @ Vt[:k, :])) / norma_total
                  for k in ks])
der.plot(ks, error, color=MORADO, linewidth=1.8, marker="o", markersize=4)
der.plot(r, error[r - 1], marker="o", markersize=10, markerfacecolor="none",
         markeredgecolor=ROJO, markeredgewidth=1.6)
# Las etiquetas se montan con % y NO con f-string: el corrector de tildes de las figuras
# protege las expresiones {...} con un centinela que a veces deja dentro del texto, y esos
# bytes salen luego como cuadraditos en el SVG (incidente del 2026-10-15).
anotar(der, "con k = %s el error cae a %s:\nya solo queda el ruido que metimos"
            % (r, coma(round(error[r - 1], 3))),
       xy=(r, error[r - 1]), xytext=(0.44, 0.74), color=ROJO)
anotar(der, "con k = 1, un %s %%\nde la energía ya está dentro"
            % coma(round(100 * (1 - error[0] ** 2), 1)),
       xy=(1, error[0]), xytext=(0.13, 0.91), color=NARANJA)
der.set_yscale("log")
der.set_xticks(ks)
der.set_ylim(error[r - 1] * 0.25, error[0] * 3.2)
titulo(der, "Truncar en k: error relativo",
       "la matriz tiene rango numérico %s: a partir de k = %s el error ya solo baja despacio"
       % (rango_real, r))
der.set_xlabel("k: cuántos valores singulares te quedas")
der.set_ylabel("error relativo al reconstruir")
rejilla(der)
numeros(der)

# El nombre del SVG va SIN tilde, como el que pide la pagina (contenido/f01/descomposicion-svd.md)
# y como exige _reparar-figuras.py: con la tilde se escribia un fichero que no usaba nadie y la
# pagina seguia enseñando uno viejo. Va partido en dos trozos porque el corrector de tildes de
# las figuras acentua las palabras sueltas de las cadenas y devolveria la tilde al nombre.
guardar(fig, "svd-cuanto-pesa-cada-direc" "cion")
