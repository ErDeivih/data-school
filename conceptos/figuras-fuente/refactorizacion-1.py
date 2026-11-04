"""refactorizacion-1.py — la red de seguridad de un refactor: la versión vieja y la nueva dan
exactamente el mismo número, y el error típico (cambiar > por >=) se ve al instante. La figura
de la pagina de refactorización (fase 11)."""

import numpy as np

from comun import *

estilo()

facturas = [
    [{"precio": 10.0, "cantidad": 3}],
    [{"precio": 25.5, "cantidad": 4}, {"precio": 0.9, "cantidad": 2}],
    [{"precio": 100.0, "cantidad": 1}],
]
etiquetas = ["3 x 10,00", "4 x 25,50\n+ 2 x 0,90", "1 x 100,00"]


def total_viejo(lineas):
    total = 0
    for linea in lineas:
        total = total + linea["precio"] * linea["cantidad"]
    if total > 100:
        total = total * 0.95
    return round(total, 2)


def total_nuevo(lineas):
    bruto = sum(linea["precio"] * linea["cantidad"] for linea in lineas)
    return round(bruto * 0.95 if bruto > 100 else bruto, 2)


# La version "descuidera": el mismo codigo con >= en lugar de >.
def total_descuidado(lineas):
    bruto = sum(linea["precio"] * linea["cantidad"] for linea in lineas)
    return round(bruto * 0.95 if bruto >= 100 else bruto, 2)


# Un poco más de ancho que antes: las dos etiquetas de cada pareja de barras (que llevan el
# mismo número) necesitan sitio para no tocarse.
fig, (izq, der) = plt.subplots(1, 2, figsize=(10.6, 4.0))

# --- Izquierda: las dos versiones dan el mismo numero en los tres casos -------------
x = np.arange(len(facturas))
viejo = [total_viejo(f) for f in facturas]
nuevo = [total_nuevo(f) for f in facturas]
ancho = 0.34
b1 = izq.bar(x - ancho / 2, viejo, ancho, color=AZUL, label="versión vieja")
b2 = izq.bar(x + ancho / 2, nuevo, ancho, color=VERDE, label="versión nueva")
# Las barras de cada pareja miden lo mismo, asi que sus dos etiquetas quedan al lado: con
# 7,5 pt hay hueco de sobra entre las dos y no se pegan.
izq.bar_label(b1, labels=[f"{v:.2f}".replace(".", ",") for v in viejo], padding=2, fontsize=7.5)
izq.bar_label(b2, labels=[f"{v:.2f}".replace(".", ",") for v in nuevo], padding=2, fontsize=7.5)
izq.set_xticks(x, etiquetas)
izq.set_ylim(0, 138)
# La leyenda vive en la franja de arriba, que queda libre por encima de las etiquetas.
titulo(izq, "Las dos versiones dan el mismo número")
izq.set_ylabel("total de la factura (EUR)")
izq.legend(loc="upper left")
rejilla(izq)
# Solo el eje y: con los dos ejes se perderian las etiquetas "3 x 10,00" del eje x.
numeros(izq, ejes="y")

# --- Derecha: el error de un caracter, visto como salto en la curva -----------------
bruto = np.linspace(80, 125, 400)
correcto = np.where(bruto > 100, bruto * 0.95, bruto)
descuidado = np.where(bruto >= 100, bruto * 0.95, bruto)
der.plot(bruto, correcto, color=AZUL, linewidth=2.0, label="con > (correcto)")
der.plot(bruto, descuidado, color=ROJO, linewidth=2.0, linestyle="--", label="con >= (el error)")
der.axvline(100, color=TEXTO, linewidth=0.8, alpha=0.5)
# El unico punto donde las dos curvas se separan: justo el bruto de 100,00 exactos.
der.plot([100], [100.0], "o", color=NARANJA, markersize=6, zorder=5)
# La esquina de arriba a la izquierda esta vacia (la curva pasa muy por debajo): la nota cabe
# ahi sin tapar ninguna linea y la leyenda se queda abajo a la derecha.
anotar(der, "a 100,00 exactos el descuidado\ncobra 95,00: 5 euros de menos",
       xy=(100, 100.0), xytext=(0.05, 0.87), color=NARANJA)
titulo(der, "El error de un carácter: un punto distinto")
der.set_xlabel("bruto de la factura (EUR)")
der.set_ylabel("total cobrado (EUR)")
der.legend(loc="lower right")
rejilla(der)
numeros(der)

guardar(fig, "refactorizacion-mismo-resultado")
