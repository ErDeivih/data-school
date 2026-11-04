"""mcp-y-servidores-de-herramientas-1.py — la forma del problema que resuelve MCP y la forma
de la solución. Arriba, el producto M por N: cada aplicación necesita su propio conector para
cada sistema, y las lineas se cruzan. Abajo, con el protocolo en medio: cada aplicación tiene
un cliente por servidor y todos hablan lo mismo. Figura de la pagina de MCP (fase 8)."""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from comun import *

estilo()

APLICACIONES = ["chat interno", "editor", "agente de incidencias"]
SISTEMAS = ["pedidos", "codigo", "ficheros"]

fig, ejes = plt.subplots(2, 1, figsize=(8.4, 7.0))


def caja(ax, x, y, ancho, alto, texto, color):
    """Rectangulo redondeado con su etiqueta centrada. Todo el diagrama va en coordenadas
    0-1, así que no depende del número de cajas."""
    ax.add_patch(FancyBboxPatch((x - ancho / 2, y - alto / 2), ancho, alto,
                                boxstyle="round,pad=0.010", linewidth=1.3,
                                edgecolor=color, facecolor=color, alpha=0.10, zorder=3))
    ax.text(x, y, texto, ha="center", va="center", fontsize=8.5, color=TEXTO, zorder=4)
    return (x, y, ancho, alto)


def conectar(ax, a, b, color, alpha, ancho=0.9, zorder=2):
    """Linea del borde derecho de la caja a al borde izquierdo de la caja b."""
    x_a, y_a, ancho_a, _ = a
    x_b, y_b, ancho_b, _ = b
    ax.plot([x_a + ancho_a / 2, x_b - ancho_b / 2], [y_a, y_b],
            color=color, alpha=alpha, linewidth=ancho, zorder=zorder, solid_capstyle="round")


def marco(ax, corto, sub):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    for lado in ax.spines.values():
        lado.set_visible(False)
    titulo(ax, corto, sub)


# --- Arriba: sin protocolo, un conector por cada pareja ------------------------
# Las columnas van desplazadas arriba y abajo a proposito: deja libre la franja central para
# escribir la cuenta, en vez de pelearse con las lineas que se cruzan.
ax = ejes[0]
filas = [0.775, 0.535, 0.295]
cajas_app, cajas_sis = [], []
for y, nombre in zip(filas, APLICACIONES):
    cajas_app.append(caja(ax, 0.16, y, 0.26, 0.13, nombre, AZUL))
for y, nombre in zip(filas, SISTEMAS):
    cajas_sis.append(caja(ax, 0.84, y, 0.24, 0.13, nombre, MORADO))

for a in cajas_app:
    for b in cajas_sis:
        conectar(ax, a, b, ROJO, 0.45)

ax.text(0.50, 0.60, "M · N = 9 conectores", ha="center", va="center", fontsize=9.5,
        color=ROJO, zorder=5, bbox=dict(facecolor="white", edgecolor="none", pad=2.2))
ax.text(0.50, 0.47, "uno distinto para cada pareja", ha="center", va="center", fontsize=8,
        color=ROJO, zorder=5, bbox=dict(facecolor="white", edgecolor="none", pad=2.2))
marco(ax, "Sin acuerdo comun: un conector por cada pareja",
      "cada aplicación tiene que saber hablar con cada sistema, por separado")

# --- Abajo: con MCP, un cliente por servidor y un protocolo comun --------------
ax = ejes[1]
filas = [0.815, 0.595, 0.375]
for y, nombre in zip(filas, APLICACIONES):
    caja(ax, 0.15, y, 0.26, 0.12, nombre, AZUL)
    # el cliente vive DENTRO del anfitrion: un conector por sesion y servidor
    ax.text(0.37, y, "cliente", ha="center", va="center", fontsize=7.5, color=AZUL)
for y, nombre in zip(filas, SISTEMAS):
    caja(ax, 0.85, y, 0.22, 0.12, nombre, MORADO)
    # la etiqueta va pegada a su caja, fuera de la banda del protocolo y de su linea
    ax.text(0.726, y - 0.038, "servidor", ha="center", va="center", fontsize=7.5, color=MORADO)

# la banda del protocolo: todo el trafico pasa por el mismo acuerdo
ax.add_patch(FancyBboxPatch((0.485, 0.30), 0.055, 0.60, boxstyle="round,pad=0.008",
                            linewidth=1.6, edgecolor=VERDE, facecolor=VERDE, alpha=0.16,
                            zorder=3))
ax.text(0.5125, 0.93, "JSON-RPC 2.0", ha="center", va="bottom", fontsize=8.5, color=VERDE)

for y in filas:
    ax.plot([0.40, 0.485], [y, y], color=VERDE, linewidth=1.1, zorder=2)
    ax.plot([0.54, 0.74], [y, y], color=VERDE, linewidth=1.1, zorder=2)

ax.text(0.5125, 0.20, "M + N = 6 piezas", ha="center", va="top", fontsize=9.5, color=VERDE)
marco(ax, "Con MCP: un cliente por servidor",
      "cada sistema se conecta una vez y el protocolo es el mismo para todos")

guardar(fig, "mcp-arquitectura-anfitrion-y-servidores")
