"""sesgo-y-etica-en-datos-1.py — las tasas de selección de los dos grupos, el liston del 80 % de
la mejor tasa y el cociente de impacto dispar. La figura de la pagina de sesgo y etica en datos
(fase 11)."""

import numpy as np

from comun import *

estilo()

# Los dos grupos del ejemplo: 420 de 1000 candidatos en A y 120 de 400 en B.
grupos = ["A", "B"]
candidatos = np.array([1000, 400])
tasa = np.array([0.42, 0.30])
liston = tasa.max() * 0.8          # el 80 % de la mejor tasa: 0,336
impacto = tasa / tasa.max()        # 1,00 para el grupo de referencia y 0,71 para el otro

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.2))

# --- Izquierda: las dos tasas y el liston por debajo del cual hay que justificar -----------
barras = izq.bar(grupos, tasa, color=[AZUL, ROJO], width=0.5)
izq.bar_label(barras, labels=[coma(t) for t in tasa], padding=3, fontsize=9)
izq.axhline(liston, color=NARANJA, linewidth=1.5, linestyle="--")
anotar(izq, "el 80 % de la mejor tasa\nes 0,336: B no llega",
       xy=(0.62, liston), xytext=(0.10, 0.95), color=NARANJA)
izq.set_ylim(0, 0.56)
izq.set_xlabel("grupo")
izq.set_ylabel("tasa de selección")
titulo(izq, "B selecciona doce puntos menos que A",
       "0,30 frente a 0,42, con el listón del 80 % en 0,336")
rejilla(izq, eje="y")
numeros(izq, ejes="y")

# --- Derecha: el cociente que se compara con 0,8 ------------------------------------------
barras = der.bar(grupos, impacto, color=[AZUL, ROJO], width=0.5)
der.bar_label(barras, labels=["1,00 (referencia)", coma(round(impacto[1], 2))], padding=3, fontsize=9)
der.axhline(0.8, color=NARANJA, linewidth=1.5, linestyle="--")
der.text(1.38, 0.82, "listón: 0,8", color=NARANJA, fontsize=8.5, ha="right")
anotar(der, "por debajo del listón:\nhay que explicar por qué",
       xy=(1.02, 0.71), xytext=(0.31, 0.92), color=ROJO)
der.set_ylim(0, 1.30)
der.set_xlabel("grupo")
der.set_ylabel("tasa del grupo / tasa del mejor")
titulo(der, "Impacto dispar: 0,71 frente a 0,8",
       "no prueba discriminación, pero obliga a revisar las variables")
rejilla(der, eje="y")
numeros(der, ejes="y")

guardar(fig, "sesgo-impacto-dispar")
