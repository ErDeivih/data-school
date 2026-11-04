"""aleatoriedad-y-muestreo-1.py — dos cosas que se confunden todo el tiempo: el error de la media
baja como 1/√n (y el muestreo estratificado lo baja más), pero el sesgo de selección no se corrige
con más muestra. Página de Aleatoriedad y muestreo (fase 10)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# --- Población sesgada de verdad: una log-normal. La media no está donde está la mayoría de los
# individuos, que es justo lo que hace peligroso el muestreo mal hecho (salarios, visitas, ventas).
POBLACION = 200_000
poblacion = azar.lognormal(0.0, 1.0, POBLACION)
media_real = float(poblacion.mean())
sigma = float(poblacion.std(ddof=1))

tamanos = np.array([10, 30, 100, 300, 1000, 3000])
REPETICIONES = 2000
columnas = {n: azar.integers(0, POBLACION, size=(REPETICIONES, n)) for n in tamanos}

# Muestreo aleatorio simple: se sortean índices y se promedian los valores.
error_simple = np.array([poblacion[columnas[n]].mean(axis=1).std(ddof=1) for n in tamanos])

# Muestreo estratificado: se parte la población en estratos por cuantiles (aquí, ordenando) y se
# reparte la muestra proporcionalmente. Al fijar cuántos individuos entran de cada tramo, se quita
# de en medio la variación que hay ENTRE estratos, que en una log-normal es casi toda.
ESTRATOS = 10
orden = np.argsort(poblacion)
bloques = np.array_split(orden, ESTRATOS)
error_estratificado = []
for n in tamanos:
    cuota = max(1, n // ESTRATOS)
    estimaciones = np.empty(REPETICIONES)
    for repeticion in range(REPETICIONES):
        elegidos = np.concatenate([azar.choice(bloque, cuota, replace=False) for bloque in bloques])
        estimaciones[repeticion] = poblacion[elegidos].mean()
    error_estratificado.append(estimaciones.std(ddof=1))
error_estratificado = np.array(error_estratificado)

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

ejes[0].loglog(tamanos, error_simple, color=AZUL, linewidth=1.8, marker="o", markersize=5,
               label="muestreo aleatorio simple")
# La teoría: σ/√n. Si los puntos se pegan a esta recta, el generador y la cuenta están bien.
ejes[0].loglog(tamanos, sigma / np.sqrt(tamanos), color=REJILLA, linewidth=1.4, linestyle="--",
               label="teoría: σ/√n")
ejes[0].loglog(tamanos, error_estratificado, color=VERDE, linewidth=1.8, marker="s",
               markersize=5, label=f"estratificado en {ESTRATOS} tramos")
ganancia = float(error_simple[-2] / error_estratificado[-2])
# Sin anotación junto a la recta teórica: la etiqueta de la leyenda ya dice qué es, y así el
# texto no se cruza con los puntos.
anotar(ejes[0], f"con n = {tamanos[-2]}, el estratificado se equivoca\n{ganancia:.1f} veces menos "
                f"con las mismas observaciones",
       xy=(float(tamanos[-2]), float(error_estratificado[-2])), xytext=(0.28, 0.90), color=VERDE)
titulo(ejes[0], "El error baja como 1/√n, y menos si estratificas",
       "media de una población log-normal, 2.000 repeticiones por tamaño")
ejes[0].set_xlabel("n: tamaño de la muestra (escala logarítmica)")
ejes[0].set_ylabel("desviación típica de la media estimada")
ejes[0].legend(loc="lower left", fontsize=8)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: el sesgo de selección. Se toma la muestra con probabilidad proporcional al valor
# (muestreo por tamaño), que es el equivalente numérico de encuestar solo a quien contesta.
TAMANO_MUESTRA, MUESTRAS = 200, 5000
pesos = poblacion / poblacion.sum()
medias_sesgadas = np.array([poblacion[azar.choice(POBLACION, TAMANO_MUESTRA, p=pesos)].mean()
                            for _ in range(MUESTRAS)])
media_sesgada = float(medias_sesgadas.mean())
sesgo = media_sesgada - media_real

ejes[1].hist(medias_sesgadas, bins=45, color=NARANJA, alpha=0.8,
             label=f"{MUESTRAS:,} muestras de tamaño {TAMANO_MUESTRA}, con selección sesgada".replace(",", "."))
# Las dos verticales van identificadas en la leyenda en vez de con anotaciones: el histograma
# ocupa el centro y cualquier texto ahí encima se lee mal.
ejes[1].axvline(media_real, color=ROJO, linewidth=2.0, label=f"media real de la población: {media_real:.2f}")
ejes[1].axvline(media_sesgada, color=VERDE, linewidth=1.8, linestyle="--",
                label=f"media de las estimaciones: {media_sesgada:.2f} "
                      f"({sesgo / media_real:.0%} por encima)")
titulo(ejes[1], "Más muestra estrecha la campana, no la centra",
       "muestreo con probabilidad proporcional al valor")
ejes[1].set_xlabel("media estimada en cada muestra")
ejes[1].set_ylabel("número de muestras")
ejes[1].legend(loc="upper left", fontsize=7.5)
rejilla(ejes[1], eje="y")
numeros(ejes[1], ejes="x")

guardar(fig, "aleatoriedad-y-muestreo-error-y-sesgo")
