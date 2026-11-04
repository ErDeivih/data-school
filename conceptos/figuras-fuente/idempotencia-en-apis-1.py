"""idempotencia-en-apis-1.py — la clave que convierte el reintento en gratis y la ventana de
tiempo en la que sigue protegiendo. La figura de la pagina de idempotencia (fase 11)."""

import numpy as np

from comun import *

estilo()

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.6, 4.2))

# --- Izquierda: tres peticiones, dos pedidos ----------------------------------------
# Cada peticion lleva su clave y el identificador de pedido que devuelve el servidor.
peticiones = ["POST k-1", "POST k-1\n(reintento)", "POST k-2"]
pedidos = [1000, 1000, 1001]
# Repetir la clave no crea un pedido nuevo: la barra se queda donde estaba.
alturas = [1, 1, 2]
colores = [AZUL, NARANJA, VERDE]

izq.bar(peticiones, alturas, color=colores, width=0.5)
for i, (alto, pedido) in enumerate(zip(alturas, pedidos)):
    izq.text(i, alto + 0.06, f"pedido {pedido}", ha="center", fontsize=9, color=TEXTO)
anotar(izq, "misma clave: devuelve\nla respuesta guardada", xy=(1, 1), xytext=(0.30, 0.62),
       color=NARANJA)
anotar(izq, "clave nueva: pedido nuevo", xy=(2, 2), xytext=(0.40, 0.20), color=VERDE)
izq.set_ylim(0, 2.6)
izq.set_yticks([0, 1, 2])
izq.set_ylabel("pedidos que existen (acumulado)")
titulo(izq, "Tres peticiones, dos pedidos",
       "el reintento devuelve la misma respuesta: 201 con id 1000")
rejilla(izq)
numeros(izq, ejes="y")

# --- Derecha: la ventana de reintentos que el TTL tiene que cubrir -------------------
# Retroceso exponencial: el intento n llega en el minuto 2**(n-1), mas el primer envio.
intentos = np.arange(1, 8)
minutos = 2.0 ** (intentos - 1)
# La linea del TTL corto: todo lo que llega despues de ahi crea un duplicado.
TTL_CORTO = 10

der.step(minutos, intentos, where="post", color=AZUL, linewidth=1.8)
der.axvline(TTL_CORTO, color=ROJO, linewidth=1.6, linestyle="--")
anotar(der, "con TTL de 10 minutos\nestos intentos duplican", xy=(20, 5.6), xytext=(0.42, 0.84),
       color=ROJO)
anotar(der, "con TTL de 24 horas\nla ventana los cubre todos", xy=(64, 7), xytext=(0.30, 0.22),
       color=VERDE)
der.set_xscale("log")
der.set_xticks([1, 2, 4, 8, 16, 32, 64])
der.set_xticklabels(["1", "2", "4", "8", "16", "32", "64"], fontsize=8.5)
der.set_xlabel("minutos desde el primer intento (escala logarítmica)")
der.set_ylabel("número de intento")
titulo(der, "El TTL tiene que cubrir la política de reintentos",
       "retroceso exponencial: 1, 2, 4, 8… minutos")
rejilla(der)
numeros(der, ejes="y")

guardar(fig, "idempotencia-clave-y-ttl")
