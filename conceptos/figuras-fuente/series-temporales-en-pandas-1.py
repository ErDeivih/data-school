"""series-temporales-en-pandas-1.py — la ventana por tiempo frente a la ventana por filas en una
serie con huecos, y cómo cambia la fecha de un agregado según la etiqueta del intervalo. Figura de
la página series-temporales-en-pandas (fase 3)."""

import numpy as np
import pandas as pd

from comun import *

estilo()

dias = [1, 2, 5, 6, 7, 8, 9, 10, 11, 12]            # faltan los dias 3 y 4
valores = [10.0, 20.0, 30.0, 40.0, 35.0, 45.0, 50.0, 42.0, 48.0, 55.0]
serie = pd.Series(valores, index=pd.to_datetime([f"2024-01-{d:02d}" for d in dias]))

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 5.4))

ejes[0].plot(dias, valores, color=TEXTO, linewidth=1.4, marker="o", markersize=3.5,
             label="observaciones")
ejes[0].plot(dias, serie.rolling("3D").sum().to_numpy(), color=AZUL, linewidth=1.8,
             label="rolling('3D'): suma por tiempo")
ejes[0].plot(dias, serie.rolling(3).sum().to_numpy(), color=ROJO, linewidth=1.8, linestyle="--",
             label="rolling(3): suma por filas")
ejes[0].axvspan(2.5, 4.5, color=REJILLA, alpha=0.22, zorder=0)
ejes[0].set_xlabel("día de enero")
ejes[0].set_ylabel("importe acumulado")
ejes[0].set_ylim(0, 200)
ejes[0].legend(loc="upper left")
titulo(ejes[0], "Con un hueco, tres filas no son tres días",
       "faltan los días 3 y 4: la ventana de filas abarca hasta cinco días")
anotar(ejes[0], "hueco: días 3 y 4", xy=(3.5, 0), xytext=(0.10, 0.48), flecha=False)
anotar(ejes[0], "mismo día: 30 frente a 60", xy=(5, 45), xytext=(0.50, 0.14))
rejilla(ejes[0])
numeros(ejes[0])

semanas = pd.Series(range(1, 11), index=pd.date_range("2024-01-01", periods=10, freq="D"))
derecha = semanas.resample("W").sum()
izquierda = semanas.resample("W", label="left", closed="left").sum()

posiciones = np.arange(3)
ancho = 0.36
ejes[1].bar(posiciones - ancho / 2, [np.nan, 28.0, 27.0], width=ancho, color=ROJO,
            label="etiqueta = domingo (por defecto)")
ejes[1].bar(posiciones + ancho / 2, [21.0, 34.0, np.nan], width=ancho, color=AZUL,
            label="etiqueta = lunes (label='left')")
ejes[1].set_xticks(posiciones, ["31 de diciembre", "7 de enero", "14 de enero"])
ejes[1].set_ylim(0, 52)
ejes[1].set_ylabel("total de la semana")
ejes[1].legend(loc="upper left")
titulo(ejes[1], "La misma semana, dos fechas distintas",
       "la etiqueta decide de qué día cuelga el total agregado")
anotar(ejes[1], "misma semana: 28 o 34", xy=(1.18, 31.5), xytext=(0.52, 0.80), color=MORADO)
print("etiquetas por defecto:", [d.strftime("%Y-%m-%d") for d in derecha.index])
print("etiquetas con label='left':", [d.strftime("%Y-%m-%d") for d in izquierda.index])
rejilla(ejes[1])
numeros(ejes[1], "y")

guardar(fig, "series-temporales-ventanas-y-etiquetas")
