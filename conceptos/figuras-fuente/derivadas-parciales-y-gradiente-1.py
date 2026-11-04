"""derivadas-parciales-y-gradiente-1.py — el gradiente apunta al máximo crecimiento (y es
perpendicular a las curvas de nivel); caminar en su contra lleva al mínimo.
Figura de la página de derivadas parciales y gradiente (fase 1)."""

import numpy as np

from comun import *

estilo()

# f(x, y) = x^2 + 2xy + 3y^2  ->  gradiente (2x + 2y, 2x + 6y)


def f(x, y):
    return x ** 2 + 2 * x * y + 3 * y ** 2


def grad(x, y):
    return np.array([2 * x + 2 * y, 2 * x + 6 * y])


xx, yy = np.meshgrid(np.linspace(-2.6, 2.6, 260), np.linspace(-3.2, 1.6, 260))
zz = f(xx, yy)
niveles = [4.0 * (1.55 ** k) for k in range(-4, 3)]      # elipses de nivel

fig, (izq, der) = plt.subplots(1, 2, figsize=(10.4, 4.6))

# --- Panel izquierdo: el mapa de la función y una flecha por cada punto ---
izq.contour(xx, yy, zz, levels=niveles, colors=REJILLA, linewidths=0.8)
malla = np.linspace(-2.2, 2.2, 9)
gx, gy = np.meshgrid(malla, np.linspace(-2.8, 1.2, 9))
uu, vv = grad(gx, gy)
norma = np.hypot(uu, vv)
izq.quiver(gx, gy, uu / norma, vv / norma, color=CIAN, scale=22, width=0.004,
           alpha=0.85, zorder=3)
izq.plot(0, 0, marker="o", color=TEXTO, markersize=5, zorder=4)
izq.annotate("cada flecha dice hacia dónde se sube más rápido\ndesde ese punto, no desde otro",
             xy=(1.9, 0.9), xytext=(-2.52, 1.42), fontsize=9, color=CIAN,
             arrowprops=dict(arrowstyle="->", color=CIAN, linewidth=0.9))
izq.annotate("el mínimo: aquí el gradiente vale (0, 0)",
             xy=(0, 0), xytext=(-2.52, -1.25), fontsize=9, color=TEXTO,
             arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9))
izq.annotate("las líneas grises son curvas de nivel:\nla flecha las cruza en ángulo recto",
             xy=(-1.28, -0.75), xytext=(-1.1, -2.5), fontsize=9, color=MORADO, ha="right",
             arrowprops=dict(arrowstyle="->", color=MORADO, linewidth=0.9))
izq.set_xlim(-2.6, 2.6)
izq.set_ylim(-3.2, 1.78)
izq.set_title("El campo de pendientes: f(x, y) = x² + 2xy + 3y²")
izq.set_xlabel("x")
izq.set_ylabel("y")
rejilla(izq, "both")
numeros(izq)

# --- Panel derecho: el descenso de gradiente sobre el mismo mapa ---
der.contour(xx, yy, zz, levels=niveles, colors=REJILLA, linewidths=0.8)
p = np.array([2.2, -3.0])
camino = [p.copy()]
for _ in range(60):
    p = p - 0.1 * grad(*p)
    camino.append(p.copy())
camino = np.array(camino)
der.plot(camino[:, 0], camino[:, 1], color=ROJO, linewidth=1.7, marker="o", markersize=2.6)
der.annotate("se empieza lejos, con el gradiente grande:\nlos primeros pasos avanzan mucho",
             xy=(camino[2, 0], camino[2, 1]), xytext=(0.35, -3.0), fontsize=9, color=ROJO,
             arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9))
der.annotate("cerca del mínimo el gradiente es diminuto:\ntras 60 pasos aún queda a "
             + coma(round(float(np.linalg.norm(camino[-1])), 3)) + " del (0, 0)",
             xy=(camino[-1, 0], camino[-1, 1]), xytext=(-2.5, -1.9), fontsize=9, color=AZUL,
             arrowprops=dict(arrowstyle="->", color=AZUL, linewidth=0.9))
der.plot(0, 0, marker="*", color=NARANJA, markersize=11, zorder=4)
der.set_xlim(-2.6, 2.6)
der.set_ylim(-3.2, 1.6)
der.set_title("Caminar en contra del gradiente es bajar")
der.set_xlabel("x")
der.set_ylabel("y")
rejilla(der, "both")
numeros(der)

guardar(fig, "gradiente-campo-y-descenso")
