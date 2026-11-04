"""poblacion-y-muestra-1.py — de dónde sale el error de muestreo y por qué el diseño de la
muestra importa más que su tamaño. Figura de la página poblacion-y-muestra."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# --- Las 15 muestras posibles de tamaño 2 en la población de seis sueldos ----------
poblacion = np.array([1200.0, 1500.0, 1800.0, 2100.0, 2400.0, 3000.0])
pares = np.array([[poblacion[i], poblacion[j]]
                  for i in range(poblacion.size) for j in range(i + 1, poblacion.size)])
medias = pares.mean(axis=1)
parametro = poblacion.mean()          # 2.000 €: el parámetro, que no se ve nunca

fig, ejes = plt.subplots(1, 2, figsize=(7.9, 3.9))

# --- Izquierda: insesgado no es acertado ------------------------------------------
eje = ejes[0]
eje.axhline(parametro, color=ROJO, linewidth=1.4, linestyle="--")
eje.scatter(np.arange(1, medias.size + 1), medias, color=AZUL, s=26, zorder=3)
eje.scatter([1], [medias[0]], color=NARANJA, s=80, zorder=4)
eje.annotate("", xy=(0.45, medias[0]), xytext=(0.45, parametro),
             arrowprops=dict(arrowstyle="<->", color=NARANJA, linewidth=1.2))
eje.annotate("esta muestra concreta falla\n650 € por debajo (un 32 %)",
             xy=(0.62, (medias[0] + parametro) / 2), xytext=(1.0, 2500),
             color=NARANJA, fontsize=8)
eje.text(15.4, 1900, "μ = 2.000 €: el parámetro", color=ROJO, fontsize=8,
         ha="right", va="top")
titulo(eje, "El estimador acierta de media, no en cada muestra",
       "las 15 medias posibles con n = 2")
eje.set_xlabel("muestra, de las 15 posibles")
eje.set_ylabel("sueldo medio (€)")
eje.set_xlim(0, 16)
rejilla(eje)
numeros(eje)

# --- Derecha: cambiar el diseño reduce el error sin medir a nadie más --------------
eje = ejes[1]
tecnicos = np.array([1800.0, 1900.0, 1850.0, 1950.0, 1820.0, 1880.0])
directivos = np.array([4100.0, 4200.0, 4150.0, 4250.0])
plantilla = np.concatenate([tecnicos, directivos])
media_real = plantilla.mean()

# Mismo n = 5 en los dos casos: uno elige al azar y el otro fuerza la representación
# de cada departamento (60 % técnicos y 40 % directivos, como en la población).
simple = np.array([azar.choice(plantilla, size=5, replace=False).mean() for _ in range(3000)])
estratificado = np.array([0.6 * azar.choice(tecnicos, size=3, replace=False).mean()
                          + 0.4 * azar.choice(directivos, size=2, replace=False).mean()
                          for _ in range(3000)])

eje.hist(simple, bins=45, density=True, color=AZUL, alpha=0.45,
         label="aleatorio simple: %.0f €" % simple.std())
eje.hist(estratificado, bins=45, density=True, color=VERDE, alpha=0.75,
         label="estratificado: %.0f €" % estratificado.std())
eje.axvline(media_real, color=ROJO, linewidth=1.4, linestyle="--")
alto = eje.get_ylim()[1]
eje.set_ylim(0, alto * 1.3)
for valor, y, color in ((simple, alto * 0.30, AZUL), (estratificado, alto * 0.62, VERDE)):
    eje.annotate("", xy=(media_real - 2 * valor.std(), y), xytext=(media_real + 2 * valor.std(), y),
                 arrowprops=dict(arrowstyle="<->", color=color, linewidth=1.3))
eje.text(media_real - 2 * simple.std(), alto * 0.33, "±2 desviaciones", color=AZUL, fontsize=8)
eje.text(media_real + 2 * estratificado.std(), alto * 0.65, "±2 desviaciones", color=VERDE,
         fontsize=8, ha="left")
titulo(eje, "El diseño reduce el error sin medir a nadie más",
       "mismo n = 5, otra forma de elegir")
eje.set_xlabel("sueldo medio de la muestra (€)")
eje.set_ylabel("densidad")
eje.legend(loc="upper left", fontsize=8)
rejilla(eje)
numeros(eje, "x")

guardar(fig, "muestra-parametro-y-diseno")
