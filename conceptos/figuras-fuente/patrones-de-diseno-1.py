"""patrones-de-diseno-1.py — que compra de verdad el patron estrategia: el cálculo de un
envio deja de ser una cadena de condicionales y pasa a ser un dato. La figura de la pagina
de patrones de diseno (fase 11)."""

import numpy as np

from comun import *

estilo()

peso = np.linspace(0, 8, 200)
estandar = 3.50 + 0.80 * peso
express = 9.00 + 2.00 * peso
gratis = np.zeros_like(peso)

# Ojo: las dos tarifas de pago NO se cruzan. Express tiene la cuota fija (9,00 frente a 3,50) y
# el precio por kilo (2,00 frente a 0,80) mas altos, asi que estandar es mas barata en todo el
# rango de pesos. El cruce solo existiria con pendientes invertidas.

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.0))

izq.plot(peso, estandar, color=AZUL, linewidth=2.0, label="estandar")
izq.plot(peso, express, color=NARANJA, linewidth=2.0, label="express")
izq.plot(peso, gratis, color=VERDE, linewidth=2.0, label="gratis")
# La separacion entre las dos rectas de pago se ensancha con el peso: eso es lo que enseña el
# panel, no un cruce que no existe.
anotar(izq, "express es más cara\nen cualquier peso",
       xy=(6.0, 21.0), xytext=(0.26, 0.42), color=NARANJA)
titulo(izq, "Cada tarifa crece a su ritmo",
       "gratis es el cero; las dos de pago no se cruzan")
izq.set_xlabel("peso del pedido (kg)")
izq.set_ylabel("coste del envio (EUR)")
izq.legend(loc="upper left")
rejilla(izq)
numeros(izq)

# Los tres casos que se calculan a mano en el ejemplo de la pagina.
pesos_caso = [2.5, 6.0]
x = np.arange(len(pesos_caso))
ancho = 0.26
valores = {
    "estandar": [3.50 + 0.80 * p for p in pesos_caso],
    "express": [9.00 + 2.00 * p for p in pesos_caso],
    "gratis": [0.0, 0.0],
}
colores = {"estandar": AZUL, "express": NARANJA, "gratis": VERDE}
for i, (nombre, alturas) in enumerate(valores.items()):
    barras = der.bar(x + (i - 1) * ancho, alturas, ancho, color=colores[nombre], label=nombre)
    # Valor encima de cada barra: sin el, dos columnas parecidas se confunden.
    der.bar_label(barras, labels=[coma(round(v, 2)) for v in alturas], padding=2, fontsize=8)
der.set_xticks(x, [coma(p) + " kg" for p in pesos_caso])
der.set_ylim(0, 32)
titulo(der, "El peso decide cuanto cuesta",
       "a 2,5 kg la estandar son 5,50 EUR; a 6 kg, 8,30 EUR")
der.set_ylabel("coste del envio (EUR)")
der.legend(loc="upper left")
rejilla(der)
# Aqui NO se llama a numeros(der): reescribiria las etiquetas "2,5 kg" del eje x.
numeros(der, ejes="y")

guardar(fig, "patrones-de-diseno-estrategia")
