"""datos-de-mercado-y-acciones-corporativas-1.py — tres vistas de la misma serie: el precio
bruto con sus saltos mecánicos, el precio ajustado y la rentabilidad acumulada. La figura de
la página de datos de mercado y acciones corporativas."""

import numpy as np
from matplotlib.dates import DateFormatter

from comun import *

estilo()

# Serie semanal de un valor con tres acciones corporativas. Es la misma del ejemplo de la
# página: 100 puntos en enero y tres eventos: split 1:2, dividendo de 1,5 puntos y contrasplit.
fechas = np.array([
    "2024-01-05", "2024-01-12", "2024-01-19", "2024-01-26",
    "2024-02-02", "2024-02-09", "2024-02-16", "2024-02-23",
    "2024-03-01", "2024-03-08", "2024-03-15", "2024-03-22", "2024-03-29",
    "2024-04-05", "2024-04-12", "2024-04-19", "2024-04-26", "2024-05-03",
], dtype="datetime64[D]")
bruto = np.array([100.0, 102.0, 99.0, 104.5,
                  106.0, 103.0, 75.0, 73.0,
                  76.0, 71.0, 69.0, 74.0, 72.0,
                  75.0, 77.0, 75.0, 78.0, 117.0])

# Cada evento es (posición del último día antes, posición de la fecha ex, dividendo en puntos,
# divisor del split): 1:2 deja el precio en la mitad (103 pasa a 75) y el contrasplit 2:3 lo
# multiplica por 1,5 (78 pasa a 117).
eventos = [(5, 6, 0.0, 0.5), (10, 11, 1.5, 1.0), (16, 17, 0.0, 1.5)]


def salto_real(i, j, div):
    """Cuánto se ha multiplicado de verdad el dinero del día i al día j: el precio del día ex
    MÁS lo repartido, partido por el precio de antes. El split no aparece aquí a propósito:
    repartir acciones no reparte dinero, así que no es un salto real."""
    return (bruto[j] + div) / bruto[i]


# Regla: cada día lleva el producto de los saltos reales de los eventos POSTERIORES a él. El
# barrido va de derecha a izquierda arrastrando ese producto, y cada evento escribe el bloque
# que va de su fecha ex hasta la fecha ex del siguiente evento. Un día nunca lleva su propio
# salto: ya lo lleva dentro el precio, y contarlo dos veces inventa una rentabilidad.
factor = np.ones(len(bruto))
acumulado = 1.0
fin = len(bruto) - 1
for i, j, div, accion in reversed(eventos):
    factor[j:fin + 1] = acumulado
    acumulado *= salto_real(i, j, div)
    fin = j - 1
factor[:fin + 1] = acumulado

# El índice se normaliza a 100 el primer día: así la última cifra ES la rentabilidad acumulada.
indice = bruto * factor
indice = indice / indice[0] * 100.0
retornos = np.concatenate([[np.nan], np.diff(indice) / indice[:-1]])
solo_precio = bruto / bruto[0] * 100.0

# El retorno del día ex está en retornos[pos], porque retornos[i] mide el salto de i-1 a i y
# pos es justo el índice de la fecha ex.
pos = [j for _, j, _, _ in eventos]

fig, ejes = plt.subplots(3, 1, figsize=(8.6, 9.6), sharex=True)

# --- 1. El precio bruto: dos escalones que no son rentabilidad ------------------
ejes[0].plot(fechas, bruto, color=ROJO, linewidth=1.6, marker="o", markersize=3)
for k, etiqueta, color in zip(pos, ["split 1:2", "dividendo de 1,5", "contrasplit 2:3"],
                              [NARANJA, MORADO, NARANJA]):
    ejes[0].axvline(fechas[k], color=color, linewidth=1.1, linestyle="--", alpha=0.85,
                    label=etiqueta)
ejes[0].set_ylabel("puntos por acción")
titulo(ejes[0], "El precio bruto salta cuando hay una acción corporativa",
       "cada salto es contabilidad, no rentabilidad: sin ajustar, la serie no sirve para medir")
rejilla(ejes[0])
numeros(ejes[0], "y")
# Un poco de aire abajo: la leyenda va en una esquina vacía y sin margen se sale del panel.
ejes[0].set_ylim(62, 124)
ejes[0].legend(loc="lower left", ncol=3)

# --- 2. El precio ajustado: la misma serie, ya comparable ----------------------
ejes[1].plot(fechas, indice, color=AZUL, linewidth=1.8, marker="o", markersize=3)
for k, div, accion in [(pos[0], 0.0, 0.5), (pos[1], 1.5, 1.0), (pos[2], 0.0, 1.5)]:
    color = NARANJA if accion != 1.0 else MORADO
    ejes[1].axvline(fechas[k], color=color, linewidth=1.1, linestyle="--", alpha=0.85)
ejes[1].set_ylabel("índice ajustado (100 = enero)")
titulo(ejes[1], "Ajustado, el día del split no cambia nada",
       "el reparto de acciones deja el índice plano; solo el dividendo mueve la cifra")
# Cada fecha ex lleva el salto real de ese día, en porcentaje sobre la serie ajustada.
etiquetas = [
    f"split: {retornos[pos[0]]:+.2%} ese día",
    f"dividendo: {retornos[pos[1]]:+.2%} ese día",
    f"contrasplit: {retornos[pos[2]]:+.2%} ese día",
]
for texto, color in zip(etiquetas, [NARANJA, MORADO, NARANJA]):
    ejes[1].plot([], [], color=color, linewidth=1.1, linestyle="--", label=texto)
rejilla(ejes[1])
numeros(ejes[1], "y")
# El techo se sube para que la leyenda quepa ARRIBA sin tocar la curva: si se queda en 108,
# la caja de la leyenda tapa el tramo de marzo.
ejes[1].set_ylim(86, 113)
ejes[1].legend(loc="upper left", fontsize=8)

# --- 3. Lo que se gana o se pierde de verdad -----------------------------------
ejes[2].plot(fechas, indice, color=VERDE, linewidth=1.8, marker="o", markersize=3,
             label="con el dividendo cobrado (ajustado)")
ejes[2].plot(fechas, solo_precio, color=REJILLA, linewidth=1.6, linestyle="--",
             label="solo el precio, sin cobrar el dividendo")
ejes[2].axhline(100, color=TEXTO, linewidth=0.8)
ejes[2].set_ylabel("nivel del índice")
ejes[2].xaxis.set_major_formatter(DateFormatter("%d-%b"))
titulo(ejes[2], "Sin el dividendo, la cuenta sale 19 puntos corta",
       "el dividendo se lo lleva quien tenía la acción el día ex, no el precio")
ejes[2].legend(loc="lower left")
rejilla(ejes[2])
numeros(ejes[2], "y")

guardar(fig, "datos-de-mercado-acciones-bruto-ajustado-acumulada")

# Los números que cita la página, calculados aquí y no escritos a mano.
print("fecha        bruto    factor  índice   salto bruto  salto ajustado")
for i, f in enumerate(fechas):
    r_bruto = "" if i == 0 else f"{bruto[i] / bruto[i - 1] - 1:+.4f}"
    r_aj = "" if i == 0 else f"{retornos[i]:+.4f}"
    print(f"{str(f)}  {bruto[i]:6.1f}  {factor[i]:7.4f}  {indice[i]:8.3f}   {r_bruto:>8s}      {r_aj:>8s}")
print()
print("salto real de cada evento", [f"{salto_real(i, j, d):.4f}" for i, j, d, c in eventos])
print("índice final             ", f"{indice[-1]:.4f}")
print("solo el precio final     ", f"{solo_precio[-1]:.4f}")
print("total con el dividendo   ", f"{indice[-1] / indice[0] - 1:+.4f}")
print("total solo el precio     ", f"{bruto[-1] / bruto[0] - 1:+.4f}")
print("salto bruto en el split  ", f"{bruto[pos[0]] / bruto[pos[0] - 1] - 1:+.4f}",
      " ajustado", f"{retornos[pos[0]]:+.4f}")
print("salto bruto en el dividendo", f"{bruto[pos[1]] / bruto[pos[1] - 1] - 1:+.4f}",
      " ajustado", f"{retornos[pos[1]]:+.4f}")
print("salto bruto en el contrasplit", f"{bruto[pos[2]] / bruto[pos[2] - 1] - 1:+.4f}",
      " ajustado", f"{retornos[pos[2]]:+.4f}")
print("volatilidad sin ajustar  ", f"{np.nanstd(np.concatenate([[np.nan], np.diff(bruto) / bruto[:-1]])):.4f}")
print("volatilidad ajustada     ", f"{np.nanstd(retornos):.4f}")
