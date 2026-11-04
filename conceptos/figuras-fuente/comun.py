"""comun.py — estilo comun de las figuras del portal.

Cada figura es un script autonomo que importa esto y llama a guardar(). Los colores son
CENTINELAS: generar-figuras.mjs los cambia por variables CSS del portal, de modo que la
misma figura se lee bien en tema claro y en tema oscuro sin duplicar ficheros.

    from comun import *
    estilo()
    fig, ax = plt.subplots()
    ax.plot(x, y, color=AZUL)
    números(ax)
    guardar(fig, "mi-figura")
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

SALIDA = Path(__file__).resolve().parent.parent / "web" / "figuras"

# Centinelas (no cambiar sin cambiar tambien CENTINELAS en generar-figuras.mjs).
TEXTO = "#101418"
REJILLA = "#9aa4b2"
AZUL = "#2563eb"
ROJO = "#dc2626"
VERDE = "#059669"
NARANJA = "#d97706"
MORADO = "#7c3aed"
CIAN = "#0891b2"
ROSA = "#db2777"


def estilo():
    """Fija el aspecto comun: sin marco por arriba ni por la derecha, rejilla suave."""
    plt.rcParams.update({
        "figure.figsize": (7.0, 3.6),
        "figure.dpi": 110,
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "axes.edgecolor": TEXTO,
        "axes.labelcolor": TEXTO,
        "axes.titlecolor": TEXTO,
        "text.color": TEXTO,
        "xtick.color": TEXTO,
        "ytick.color": TEXTO,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "grid.color": REJILLA,
        "grid.alpha": 0.45,
        "grid.linewidth": 0.7,
        "legend.frameon": False,
        "legend.fontsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.constrained_layout.use": True,
        "svg.fonttype": "none",
    })


def coma(x, _pos=None):
    """Numeros con coma decimal, como se escriben en el portal."""
    return ("%g" % x).replace(".", ",")


def numeros(ax, ejes="both"):
    """Pone la coma decimal en los ejes indicados."""
    fmt = FuncFormatter(coma)
    if ejes in ("x", "both"):
        ax.xaxis.set_major_formatter(fmt)
    if ejes in ("y", "both"):
        ax.yaxis.set_major_formatter(fmt)
    return ax


def rejilla(ax, eje="y"):
    ax.grid(True, axis=eje, zorder=0)
    ax.set_axisbelow(True)
    return ax


def guardar(fig, nombre):
    """Escribe web/figuras/<nombre>.svg y lo dice por pantalla.

    Si la variable de entorno FIGURAS_PNG apunta a una carpeta, guarda además una copia PNG
    con el mismo encuadre. Sirve para revisar la figura a ojo (y para pegarla en un documento);
    el portal sigue usando solo el SVG.
    """
    import os

    SALIDA.mkdir(parents=True, exist_ok=True)
    fig.savefig(SALIDA / (nombre + ".svg"), format="svg", transparent=True, bbox_inches="tight")
    destino_png = os.environ.get("FIGURAS_PNG")
    if destino_png:
        from pathlib import Path as _Path

        carpeta = _Path(destino_png)
        carpeta.mkdir(parents=True, exist_ok=True)
        fig.savefig(carpeta / (nombre + ".png"), format="png", dpi=150, bbox_inches="tight",
                    facecolor="white")
    plt.close(fig)
    print(nombre + ".svg")


def titulo(ax, corto, sub=None):
    """Título CORTO (hasta unos 50 caracteres) y, si hay más que decir, una línea pequeña
    debajo. Los títulos largos se solapan con los ejes: medido el 2026-10-15, 51 de 64
    figuras tenían algún título de más de 52 caracteres.

    El subtítulo va pegado al borde de arriba del eje (y=1.012) y el título se sube con
    `pad` para dejarle sitio: sin ese margen los dos se escriben uno encima del otro."""
    if not sub:
        ax.set_title(corto)
        return
    ax.set_title(corto, pad=20)
    ax.text(0.5, 1.012, sub, transform=ax.transAxes, ha="center", va="bottom",
            fontsize=8.5, color=REJILLA)


def anotar(ax, texto, xy, xytext, color=None, flecha=True, align="left", fondo=False):
    """Anotación con el texto en coordenadas del eje (0-1) en vez de en coordenadas de datos:
    así cae en una zona vacía y no se pisa con la curva. `xy` es el punto que se señala (en
    datos) y `xytext` dónde se escribe (en fracción de eje, por ejemplo (0.05, 0.9)).

    `align` es "left" (por defecto) o "right": con "right" el texto se pega a su derecha, que
    es lo que hace falta para escribir una nota contra el borde derecho del eje sin salirse.

    `fondo=True` pone un rectángulo blanco detrás del texto: solo para cuando ha sido imposible
    encontrar un hueco libre y la nota tiene que cruzar una línea. El blanco es el del papel (no
    un color del tema) y por eso no lo cambia `generar-figuras.mjs`."""
    ha = "right" if align == "right" else "left"
    ax.annotate(texto, xy=xy, xycoords="data", xytext=xytext, textcoords="axes fraction",
                fontsize=8.5, color=color or TEXTO, va="center", ha=ha,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.0) if fondo else None,
                arrowprops=dict(arrowstyle="->", color=color or TEXTO, linewidth=0.9,
                                shrinkA=2, shrinkB=2) if flecha else None)
