"""independencia-y-condicionamiento-1.py — lo que el condicionamiento le hace a una relación.

Tres nubes de puntos con los MISMOS datos de partida (dos variables independientes): en la
primera se mira el conjunto, en la segunda se condiciona en un confusor comun y en la tercera
en un colisionador. El número que importa es r, que se escribe dentro de cada panel.
"""

import numpy as np

from comun import *

estilo()

azar = np.random.default_rng(7)
n = 400

# Una sola variable latente manda en todo: de ella salen los confusores y los colliders.
temperatura = azar.normal(0, 1, n)
helados = temperatura + azar.normal(0, 0.8, n)      # sube con el calor
ahogamientos = temperatura + azar.normal(0, 0.8, n)  # sube con el calor, y nada mas

# Dos filas de dos paneles: con tres en una fila cada uno queda estrecho y el texto no cabe.
# El cuarto hueco lleva el resumen de los tres valores de r, que es lo que hay que comparar.
fig, ejes = plt.subplots(2, 2, figsize=(10.6, 7.4))
(e0, e1), (e2, e3) = ejes

# --- Panel 1: la relacion marginal, sin condicionar en nada ----------------------
r_marginal = np.corrcoef(helados, ahogamientos)[0, 1]
e0.scatter(helados, ahogamientos, s=13, color=ROJO)
# La nube va en diagonal: la esquina de arriba a la izquierda y la de abajo a la derecha
# quedan libres, una para cada texto.
anotar(e0, f"r = {r_marginal:.2f}".replace(".", ","),
       xy=(helados.mean(), ahogamientos.mean()), xytext=(0.03, 0.93), color=ROJO, flecha=False)
anotar(e0, "pero la causa es otra", xy=(helados.mean(), ahogamientos.mean()),
       xytext=(0.62, 0.06), flecha=False)
e0.set_xlabel("helados vendidos")
e0.set_ylabel("ahogamientos")
titulo(e0, "Sin condicionar: parecen relacionados")
numeros(e0)
rejilla(e0)

# --- Panel 2: condicionar en el confusor (la temperatura) ------------------------
corte = np.median(temperatura)
frios, calidos = temperatura <= corte, temperatura > corte
rs = []
for grupo in (frios, calidos):
    e1.scatter(helados[grupo], ahogamientos[grupo], s=13,
               color=AZUL if grupo is frios else NARANJA)
    rs.append(np.corrcoef(helados[grupo], ahogamientos[grupo])[0, 1])
r_dentro = float(np.mean(rs))
# Aqui la nube se parte en dos grupos a lo largo de la diagonal: los textos van a los lados.
anotar(e1, f"r dentro de cada grupo = {r_dentro:.2f}".replace(".", ","),
       xy=(helados.mean(), ahogamientos.mean()), xytext=(0.03, 0.93), color=AZUL, flecha=False)
anotar(e1, "azul días fríos, naranja días cálidos", xy=(helados.mean(), ahogamientos.mean()),
       xytext=(0.44, 0.06), flecha=False)
e1.set_xlabel("helados vendidos")
e1.set_ylabel("ahogamientos")
titulo(e1, "Condicionar en la temperatura", "la relación entre las dos variables se va")
numeros(e1)
rejilla(e1)

# --- Panel 3: condicionar en el colisionador (estar ingresado) --------------------
p = 0.10
a = azar.random(n) < p          # enfermedad A, independiente de B
b = azar.random(n) < p          # enfermedad B
ingresa = a | b                 # el ingreso es consecuencia de cualquiera de las dos
r_poblacion = np.corrcoef(a.astype(float), b.astype(float))[0, 1]
r_hospital = np.corrcoef(a[ingresa].astype(float), b[ingresa].astype(float))[0, 1]

# Un poco de ruido solo para que los 4 puntos de la muestra no queden apilados.
jitter = lambda v: v + azar.normal(0, 0.045, len(v))
e2.scatter(jitter(a), jitter(b), s=13, color=REJILLA)
e2.scatter(jitter(a[ingresa]), jitter(b[ingresa]), s=15, color=MORADO)
e2.set_xticks([0, 1]); e2.set_yticks([0, 1])
e2.set_xticklabels(["no tiene A", "tiene A"])
e2.set_yticklabels(["no tiene B", "tiene B"])
e2.set_ylim(-0.55, 1.12)
e2.set_xlabel("enfermedad A")
e2.set_ylabel("enfermedad B")
# Los cuatro grupos estan en las esquinas: el centro del panel esta vacio y ahi caben las notas.
e2.text(0.5, 0.62, f"r en la población = {r_poblacion:+.2f}".replace(".", ","),
        transform=e2.transAxes, ha="center", va="center", fontsize=9, color=TEXTO)
e2.text(0.5, 0.50, f"r entre los ingresados = {r_hospital:+.2f}".replace(".", ","),
        transform=e2.transAxes, ha="center", va="center", fontsize=9, color=MORADO)
e2.text(0.5, 0.30, "los ingresados llevan\nuno de los dos cuadros",
        transform=e2.transAxes, ha="center", va="center", fontsize=9, color=MORADO)
titulo(e2, "Condicionar en el ingreso", "la relación entre las dos variables aparece")
numeros(e2)

# --- Panel 4: los tres valores de r, juntos para poder compararlos ----------------
e3.axis("off")
titulo(e3, "Los tres casos, de un vistazo", "el mismo dato: solo cambia en qué se condiciona")
filas = [("sin condicionar nada", r_marginal, ROJO),
         ("condicionando en la temperatura", r_dentro, AZUL),
         ("condicionando en el ingreso", r_hospital, MORADO)]
for k, (texto, valor, color) in enumerate(filas):
    y = 0.62 - 0.20 * k
    e3.text(0.04, y, texto, transform=e3.transAxes, fontsize=10, va="center", color=TEXTO)
    e3.text(0.96, y, f"r = {valor:+.2f}".replace(".", ","), transform=e3.transAxes,
            fontsize=10, va="center", ha="right", color=color)

# El nombre del fichero SVG va en ASCII, sin tildes: es el que pide la pagina
# (contenido/f01/independencia-y-condicionamiento.md) y el que comprueba _reparar-figuras.py.
guardar(fig, "independencia-condicionar-cambia-la-relación")
