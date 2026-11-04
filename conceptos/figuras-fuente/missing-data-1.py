"""missing-data-1.py — los dos errores de los datos ausentes, medidos sobre una nomina.

Izquierda: los que más ganan no contestan, así que la media de los que responden no es la
media de la plantilla. Derecha: rellenar los huecos con esa media deja un pico enorme en el
centro y la dispersión se hunde: el resultado parece preciso y no lo es.
La figura de la pagina de datos ausentes (fase 2)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)
n = 4000
sueldo = azar.lognormal(mean=7.95, sigma=0.40, size=n)     # cola larga hacia arriba
corte = float(np.quantile(sueldo, 0.75))
responden = sueldo < corte                                 # los que mas ganan no contestan
observado = sueldo[responden]

media_real = float(sueldo.mean())
media_obs = float(observado.mean())
desv_real = float(sueldo.std())
columna = sueldo.copy()
columna[~responden] = media_obs
desv_col = float(columna.std())


def miles(x):
    """Miles con punto, como se escriben en el portal: 3040 -> 3.040."""
    entero = "%d" % round(x)
    return entero if len(entero) <= 3 else entero[:-3] + "." + entero[-3:]


fig, ejes = plt.subplots(1, 2, figsize=(10.2, 4.4))
bordes = np.linspace(sueldo.min(), sueldo.max(), 46)
cuenta_real, _ = np.histogram(sueldo, bins=bordes)

# --- Panel 1: borrar las filas que faltan mueve la media ------------------------------
ejes[0].hist(sueldo, bins=bordes, color=AZUL, alpha=0.32, label="toda la plantilla")
ejes[0].hist(observado, bins=bordes, color=NARANJA, alpha=0.55, label="los que contestan")
ejes[0].axvline(media_real, color=ROJO, linewidth=1.8)
ejes[0].axvline(media_obs, color=MORADO, linewidth=1.8, linestyle="--")
anotar(ejes[0], "media real " + miles(media_real) + " €",
       xy=(media_real, cuenta_real.max() * 0.50), xytext=(0.44, 0.95), color=ROJO)
anotar(ejes[0], "media de los que contestan " + miles(media_obs) + " €\n(se queda "
       + miles(media_real - media_obs) + " € por debajo)",
       xy=(media_obs, cuenta_real.max() * 0.30), xytext=(0.44, 0.78), color=MORADO)
anotar(ejes[0], "el hueco que falta está en la cola\nde la derecha, no repartido al azar",
       xy=(sueldo.max() * 0.92, cuenta_real.max() * 0.10), xytext=(0.44, 0.42), color=TEXTO)
titulo(ejes[0], "Si no contestan los que más ganan, la media baja",
       "borrar las filas ausentes estima a los que responden, no a la plantilla")
ejes[0].set_xlabel("sueldo mensual (€)")
ejes[0].set_ylabel("personas")
ejes[0].legend(loc="center right", fontsize=8.5)
numeros(ejes[0])
rejilla(ejes[0])

# --- Panel 2: imputar por la media aplasta la dispersion ------------------------------
ejes[1].hist(sueldo, bins=bordes, histtype="step", color=AZUL, linewidth=1.6,
             label="toda la plantilla")
ejes[1].hist(columna, bins=bordes, color=ROSA, alpha=0.55, label="imputando por la media")
ejes[1].set_ylim(0, cuenta_real.max() * 1.9)
ejes[1].axhline(cuenta_real.max() * 1.9, color=REJILLA, linewidth=0.8, linestyle=":")
anotar(ejes[1], miles(float(np.sum(~responden))) + " personas con el mismo sueldo:\n"
       "la barra se sale del gráfico",
       xy=(media_obs, cuenta_real.max() * 1.85), xytext=(0.30, 0.62), color=ROSA)
ejes[1].text(0.03, 0.97, "desviación típica real: " + miles(desv_real) + " €",
             transform=ejes[1].transAxes, va="top", color=AZUL, fontsize=9.5)
ejes[1].text(0.03, 0.88, "con la media imputada: " + miles(desv_col) + " €",
             transform=ejes[1].transAxes, va="top", color=ROSA, fontsize=9.5)
titulo(ejes[1], "Imputar por la media: un pico en el centro",
       "el mismo valor en todos los huecos encoge la dispersión y finge precisión")
ejes[1].set_xlabel("sueldo mensual (€)")
ejes[1].set_ylabel("personas")
ejes[1].legend(loc="center right", fontsize=8.5)
numeros(ejes[1])
rejilla(ejes[1])

guardar(fig, "nulos-sesgo-y-varianza")
