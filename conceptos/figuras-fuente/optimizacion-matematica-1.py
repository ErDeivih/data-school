"""optimizacion-matematica-1.py — dónde está el óptimo de un programa lineal (en un vértice, y el
gradiente no lo respeta) y cómo el paso decide si el descenso converge, se arrastra o se escapa.
Página de Optimización matemática (fase 10)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

# --- Izquierda: la región factible de «maximizar 2x + 3y con x + y ≤ 4, x + 3y ≤ 6, x, y ≥ 0».
# El polígono se dibuja calculando, para cada x, el intervalo de y que cumple las tres
# restricciones: es la forma correcta de rellenar una región convexa descrita por desigualdades.
x = np.linspace(0, 4.6, 600)
y_min = np.maximum(0.0, np.zeros_like(x))
y_max = np.minimum(4 - x, (6 - x) / 3)
dentro = y_max >= y_min
ejes[0].fill_between(x[dentro], y_min[dentro], y_max[dentro], color=AZUL, alpha=0.13)
ejes[0].plot(x, 4 - x, color=AZUL, linewidth=1.6, label="x + y ≤ 4")
ejes[0].plot(x, (6 - x) / 3, color=NARANJA, linewidth=1.6, label="x + 3y ≤ 6")

# Los vértices y el valor del objetivo en cada uno: el óptimo de un programa lineal está siempre
# en uno de estos puntos, nunca en el interior.
vertices = [(0.0, 0.0), (4.0, 0.0), (0.0, 2.0), (3.0, 1.0)]
for vx, vy in vertices:
    valor = 2 * vx + 3 * vy
    ejes[0].plot(vx, vy, marker="o", markersize=6, color=TEXTO, zorder=5)
    # El rótulo del origen se aparta hacia arriba para no salirse por el borde inferior.
    desvio = (0.14, 0.16) if (vx, vy) == (0.0, 0.0) else (0.12, 0.14)
    ejes[0].annotate(f"{valor:.0f}", xy=(vx, vy), xytext=(vx + desvio[0], vy + desvio[1]),
                     fontsize=9, color=TEXTO)
opt_x, opt_y = 3.0, 1.0
ejes[0].plot(opt_x, opt_y, marker="o", markersize=11, color=ROJO, zorder=6)

# Descenso de gradiente sobre la misma función objetivo: sube en la dirección (2, 3) y no ve las
# restricciones, así que se sale del polígono a las pocas iteraciones.
puntos = [(0.2, 0.2)]
for _ in range(9):
    px, py = puntos[-1]
    puntos.append((px + 0.6 * 2, py + 0.6 * 3))
puntos = np.array(puntos)
ejes[0].plot(puntos[:, 0], puntos[:, 1], color=VERDE, linewidth=1.8, marker="o", markersize=4)
anotar(ejes[0], f"el óptimo está en un vértice: {2 * opt_x + 3 * opt_y:.0f} en (3, 1)",
       xy=(opt_x, opt_y), xytext=(0.10, 0.90), color=ROJO)
anotar(ejes[0], "el gradiente no ve las restricciones:\nse sale de la región factible",
       xy=(float(puntos[4, 0]), float(puntos[4, 1])), xytext=(0.42, 0.26), color=VERDE)
titulo(ejes[0], "El óptimo de un programa lineal es un vértice",
       "la misma función objetivo, con restricciones y sin mirarlas")
ejes[0].set_xlabel("x")
ejes[0].set_ylabel("y")
ejes[0].set_xlim(0, 6.4)
ejes[0].set_ylim(0, 4.6)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")
# Sin leyenda: la trayectoria verde va rotulada con su propia anotación y así el vértice (4, 0)
# se lee sin nada encima.

# --- Derecha: el mismo problema con cuatro pasos distintos. Se dibuja la distancia al mínimo,
# que es lo que el paso decide: si baja, si se queda oscilando o si se dispara. En escala
# logarítmica la convergencia es una recta y la divergencia también, pero el mínimo exacto no se
# puede pintar (el logaritmo de cero no existe), así que el eje se corta en 1e-12 y se avisa.
iteraciones = np.arange(0, 31)
distancias = {}
for eta, color, estilo_linea, etiqueta in [
    (0.05, AZUL, "-", "η = 0,05: converge, pero despacio"),
    (0.40, VERDE, "-", "η = 0,40: se planta en el mínimo"),
    (0.95, NARANJA, ":", "η = 0,95: oscila cada vez menos"),
    (1.05, ROJO, ":", "η = 1,05: diverge"),
]:
    xs = [0.0]
    for _ in iteraciones[1:]:
        xs.append(xs[-1] - eta * (2 * xs[-1] - 4))
    distancia = np.abs(np.array(xs) - 2.0)
    distancias[eta] = distancia
    # Las distancias por debajo del corte no se pintan: en escala logarítmica no hay sitio para
    # el cero y el hueco se leería como un salto de la curva.
    visible = distancia > 1e-12
    ejes[1].plot(iteraciones[visible], distancia[visible], color=color, linewidth=1.8,
                 linestyle=estilo_linea, marker="o", markersize=3, label=etiqueta)

# En escala logarítmica la curva divergente domina el eje y aplasta las otras tres contra el
# suelo. El eje se ajusta a las que convergen y la divergente se recorta contra el borde: el
# mensaje de que se escapa sigue leyéndose en la anotación.
limite = 3 * float(max(distancias[0.05].max(), distancias[0.95].max()))
ejes[1].set_ylim(5e-4, limite)
anotar(ejes[1], "aquí el paso es demasiado grande:\ncada iteración se aleja del mínimo",
       xy=(28.0, 0.92 * limite), xytext=(0.97, 0.93), color=ROJO, align="right")
anotar(ejes[1], "la condición es η < 2/L y aquí L = 2,\nasí que η < 1",
       xy=(25.0, float(distancias[0.95][25])), xytext=(0.22, 0.42), color=TEXTO)
titulo(ejes[1], "El paso decide si converge o se escapa",
       "distancia al mínimo, en escala logarítmica")
ejes[1].set_xlabel("iteración")
ejes[1].set_ylabel("distancia al mínimo (escala logarítmica)")
ejes[1].set_yscale("log")
ejes[1].legend(loc="lower left", fontsize=8)
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="x")

guardar(fig, "optimizacion-matematica-poliedro-y-paso")
