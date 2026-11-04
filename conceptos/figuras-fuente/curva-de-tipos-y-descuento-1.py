"""curva-de-tipos-y-descuento-1.py — la curva de tipos por plazo y lo que un punto de subida
hace al precio segun el vencimiento. La figura de la pagina de curva de tipos y descuento
(fase 9)."""

import numpy as np

from comun import *

estilo()

# La curva de la tabla de la pagina: incluye los plazos 1, 2, 5 y 10 que se citan en el texto
# (2,50 % / 2,80 % / 3,20 % / 3,60 %) y crece sin saltos raros entre medias.
plazos = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
tipos = np.array([0.0250, 0.0280, 0.0300, 0.0310, 0.0320, 0.0330, 0.0340, 0.0350, 0.0355, 0.0360])

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.4))

# --- Izquierda: la curva y el descuento que implica ---------------------------------
izq.plot(plazos, 100 * tipos, color=AZUL, linewidth=2.0, marker="o", markersize=5)
# La banda ayuda a leer "no hay un tipo, hay un tipo por plazo".
izq.fill_between(plazos, 0, 100 * tipos, color=AZUL, alpha=0.10)
df10 = 1 / (1 + tipos[-1]) ** plazos[-1]
anotar(izq, "a 10 anos el dinero se paga\nmas caro que a 1: la curva sube", xy=(8, 100 * tipos[7]),
       xytext=(0.20, 0.80), color=AZUL)
anotar(izq, "DF(10) = %.4f: un euro de dentro\nde 10 anos vale hoy 70 centimos" % df10,
       xy=(10, 100 * tipos[-1]), xytext=(0.24, 0.20), color=MORADO)
izq.set_xlim(0.5, 10.8)
izq.set_ylim(0, 6.4)
izq.set_xlabel("plazo en anos")
izq.set_ylabel("tipo al contado (%)")
titulo(izq, "La curva de tipos: un tipo para cada plazo",
       "prestar más tiempo exige más compensación")
rejilla(izq)
numeros(izq, ejes="both")

# --- Derecha: mismo punto de subida, vencimientos muy distintos ---------------------
vencimientos = np.array([1, 2, 5, 10, 20])
z_base, z_nuevo = 0.03, 0.04
precio_antes = 1 / (1 + z_base) ** vencimientos
precio_despues = 1 / (1 + z_nuevo) ** vencimientos
# El signo es negativo (el precio cae): se dibuja en valor absoluto y el signo va en la etiqueta,
# porque una barra hacia abajo con el eje en positivo no se ve.
perdida = 100 * (1 - precio_despues / precio_antes)

barras = der.bar(np.arange(vencimientos.size), perdida, color=ROJO, width=0.55)
# El eje x lleva posiciones numericas y las etiquetas se ponen aparte: con cadenas, las
# coordenadas de las anotaciones dejan de ser datos y las barras se colocan donde no toca.
der.set_xticks(np.arange(vencimientos.size))
der.set_xticklabels([str(v) for v in vencimientos])
der.bar_label(barras, labels=["-%.2f" % v for v in perdida], padding=3, fontsize=8.5,
              label_type="edge", bbox=dict(facecolor="white", edgecolor="none", pad=0.6))
anotar(der, "el mismo punto de tipos:\ncae 9,6 veces más a 10 anos", xy=(3, perdida[3]),
       xytext=(0.30, 0.78), color=ROJO)
anotar(der, "a 1 ano casi no se nota", xy=(0, perdida[0]), xytext=(0.10, 0.46), color=VERDE)
der.set_xlabel("vencimiento en anos")
der.set_ylabel("caida del precio (%)")
der.set_ylim(0, 45)
titulo(der, "El mismo punto de tipos no duele igual",
       "cupon cero del 3 % al 4 %: el plazo manda")
rejilla(der)
numeros(der, ejes="y")

guardar(fig, "curva-tipos-y-descuento")
