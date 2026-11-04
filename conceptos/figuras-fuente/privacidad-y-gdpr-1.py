"""privacidad-y-gdpr-1.py — el tamaño de cada grupo de cuasi-identificadores antes y después de
generalizar la fecha, y las tres salidas posibles cuando k = 2 no se cumple. La figura de la
pagina de privacidad y RGPD (fase 11)."""

import numpy as np

from comun import *

estilo()

K = 2

# --- Izquierda: los cuatro usuarios del ejemplo, agrupados por sus cuasi-identificadores ---
# Tres combinaciones de (codigo postal, nacimiento), con 2, 1 y 1 usuarios cada una.
etiquetas = ["28001\n1980-03-02", "28001\n1991-07-15", "28013\n1975-11-30"]
fecha_exacta = np.array([2, 1, 1])
solo_anio = np.array([2, 1, 1])     # pasar del dia al ano deja los grupos igual de pequenos

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.4))

x = np.arange(len(etiquetas))
ancho = 0.36
b1 = izq.bar(x - ancho / 2, fecha_exacta, width=ancho, color=AZUL, label="fecha exacta")
b2 = izq.bar(x + ancho / 2, solo_anio, width=ancho, color=NARANJA, label="solo el año")
izq.bar_label(b1, padding=3, fontsize=9)
izq.bar_label(b2, padding=3, fontsize=9)
izq.axhline(K, color=ROJO, linewidth=1.5, linestyle="--")
anotar(izq, "k = 2: ningún grupo puede\nquedarse por debajo",
       xy=(1.15, K), xytext=(0.04, 0.86), color=ROJO)
izq.set_xticks(x, etiquetas)
izq.set_ylim(0, 3.6)
izq.set_ylabel("usuarios por combinación")
izq.set_xlabel("(código postal, nacimiento)")
titulo(izq, "Antes y después de generalizar la fecha",
       "los grupos siguen siendo 2, 1 y 1: dos personas están solas")
izq.legend(loc="upper right", bbox_to_anchor=(1.0, 0.74))
rejilla(izq, eje="y")
numeros(izq, ejes="y")

# --- Derecha: que se puede publicar con k = 2 y que cuesta cada salida ---------------------
# Publicar tal cual expone a las dos personas que estan solas; suprimir esas filas cumple
# k = 2 publicando la mitad; agregar todo cumple de sobra pero deja una sola fila.
opciones = ["publicar\ntal cual", "suprimir\nlas filas únicas", "agregar\ntodo"]
filas = np.array([4, 2, 1])
k_resultante = ["k = 1", "k = 2", "k = 4"]
colores = [ROJO, NARANJA, VERDE]

barras = der.bar(opciones, filas, color=colores, width=0.5)
der.bar_label(barras, labels=[f"{f} filas · {k}" for f, k in zip(filas, k_resultante)],
              padding=4, fontsize=9)
der.axhline(K, color=TEXTO, linewidth=1.1, linestyle="--")
der.text(2.38, K + 0.12, "mínimo que exige k = 2", color=TEXTO, fontsize=8.5, ha="right")
der.set_ylim(0, 5.4)
der.set_ylabel("filas que se publican")
titulo(der, "Cumplir k = 2 cuesta filas o detalle",
       "cada salida cambia lo que se aprende de los cuatro usuarios")
rejilla(der, eje="y")
numeros(der, ejes="y")

guardar(fig, "privacidad-k-anonimato")
