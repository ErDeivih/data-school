"""autenticacion-y-autorizacion-1.py — el diseño entero de una función de derivación de
contraseñas: pasar de microsegundos a decenas de milisegundos por intento. La figura de la
página de autenticación y autorización (fase 11)."""

import numpy as np

from comun import *

estilo()

# Órdenes de magnitud representativos por núcleo: sha256 va a ~5 millones de intentos por
# segundo y scrypt con n=2**14 a unas 17. El código de la página los mide al ejecutarse.
sha256_por_segundo = 5e6
scrypt_por_segundo = 17.0
candidatas = 1e9

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 3.8))

# --- Izquierda: intentos por segundo ------------------------------------------------
nombres = ["sha256\n(hash rápido)", "scrypt n=2**14\n(derivación lenta)"]
velocidad = np.array([sha256_por_segundo, scrypt_por_segundo])
barras = izq.barh(nombres, velocidad, color=[ROJO, VERDE], height=0.55)
izq.set_xscale("log")
izq.bar_label(barras, labels=["5.000.000 por segundo", "17 por segundo"],
              padding=4, fontsize=9)
izq.set_xlim(1, 5e8)
# Ejes logarítmicos: sin numeros(), porque la coma decimal del portal no se lee en potencias.
izq.set_xticks([1, 1e3, 1e6], ["1", "1.000", "1.000.000"])
izq.set_xlabel("intentos por segundo y por núcleo")
titulo(izq, "Lo que cuesta probar una candidata",
       "cinco millones por segundo frente a 17, por núcleo")
rejilla(izq, eje="x")

# --- Derecha: lo que tarda en caer una contraseña ------------------------------------
# Probar mil millones de candidatas (una contraseña de 9 caracteres mal elegida).
segundos = candidatas / np.array([sha256_por_segundo, scrypt_por_segundo])
barras = der.barh(nombres, segundos, color=[ROJO, VERDE], height=0.55)
der.set_xscale("log")
der.bar_label(barras, labels=["200 s (3,3 minutos)", "58.000.000 s (unos 2 años)"],
              padding=4, fontsize=9)
der.set_xlim(1, 1e10)
der.set_xticks([1e2, 1e5, 1e8], ["100 s", "un día", "3 años"])
der.set_xlabel("tiempo para probar mil millones de candidatas (escala logarítmica)")
titulo(der, "Mil millones de candidatas: un café o dos años",
       "según lo que cueste cada intento")
rejilla(der, eje="x")

guardar(fig, "autenticacion-coste-de-la-contrasena")
