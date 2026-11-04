"""distribuciones-en-datos-reales-1.py — los cuatro patrones que rompen la normal:
cola gorda, dos picos, censura y exceso de ceros. La figura de la pagina de
distribuciones en datos reales (fase 5)."""

import numpy as np

from comun import *

estilo()

# --- Arriba izquierda: cola gorda --------------------------------------------
# Misma generacion que el bloque de codigo de la pagina (mismo orden de llamadas
# al generador), para que los numeros coincidan con los de la tabla del texto.
rng_pagina = np.random.default_rng(1)
rng_pagina.normal(50_000.0, 20_000.0, size=100_000)
ingresos = rng_pagina.lognormal(mean=10.8, sigma=0.6, size=100_000)
media = float(ingresos.mean())
mediana = float(np.median(ingresos))
maximo = float(ingresos.max())

# --- Arriba derecha: dos poblaciones mezcladas -------------------------------
azar = np.random.default_rng(7)
alturas = np.concatenate([azar.normal(163.0, 5.0, 7_000), azar.normal(180.0, 5.0, 3_000)])
global_ = float(alturas.mean())

# --- Abajo izquierda: censura por la derecha ---------------------------------
real = np.random.default_rng(4).lognormal(mean=1.0, sigma=0.8, size=50_000)
tope = 10.0
registrado = np.minimum(real, tope)
censurado = 100 * float((real > tope).mean())

# --- Abajo derecha: ceros de mas --------------------------------------------
# El mismo orden de llamadas al generador que el ejemplo: salen 62,7 % de ceros.
rng = np.random.default_rng(2)
visitas = np.where(rng.random(10_000) < 0.62, 0, rng.poisson(3.5, size=10_000))
sin_visita = 100 * float((visitas == 0).mean())

fig, ejes = plt.subplots(2, 2, figsize=(8.2, 6.0))

# --- Panel: cola gorda -------------------------------------------------------
ax = ejes[0, 0]
ax.hist(ingresos, bins=90, range=(0, 200_000), color=AZUL)
ax.axvline(media, color=ROJO, linewidth=1.5, linestyle="--")
ax.axvline(mediana, color=VERDE, linewidth=1.5)
ax.set_xlim(0, 200_000)
ax.set_ylim(0, 9_000)
ax.set_xlabel("ingreso mensual (miles de euros)")
ax.set_ylabel("personas")
ax.set_xticks([0, 50_000, 100_000, 150_000, 200_000], ["0", "50", "100", "150", "200"])
anotar(ax, f"la mediana, {mediana / 1000:.1f} mil", (mediana, 3000), (0.30, 0.88), color=VERDE)
anotar(ax, f"la media, {media / 1000:.1f} mil", (media, 1500), (0.52, 0.70), color=ROJO)
anotar(ax, f"la más alta llega a {maximo / 1000:,.0f} mil", (195_000, 5200), (0.97, 0.50),
       color=TEXTO, align="right")
titulo(ax, "Una cola larga arrastra la media", "más de la mitad gana menos que la media")
numeros(ax, ejes="y")
rejilla(ax)

# --- Panel: los dos picos ----------------------------------------------------
ax = ejes[0, 1]
ax.hist(alturas, bins=60, range=(145, 200), color=MORADO)
for valor, color in ((163.0, AZUL), (180.0, CIAN)):
    ax.axvline(valor, color=color, linewidth=1.3)
ax.axvline(global_, color=ROJO, linewidth=1.6, linestyle="--")
ax.set_xlim(145, 200)
ax.set_ylim(0, 640)
ax.set_xlabel("altura (cm)")
ax.set_ylabel("personas")
anotar(ax, "turno de manana", (163.0, 2400), (0.10, 0.90), color=AZUL)
anotar(ax, "turno de noche", (180.0, 1200), (0.78, 0.90), color=CIAN)
anotar(ax, f"la media global, {global_:.1f}, cae en el valle", (global_, 585), (0.97, 0.84),
       color=ROJO, align="right")
titulo(ax, "Dos picos: la media no esta en ninguno", "el promedio cae donde casi no hay nadie")
numeros(ax)
rejilla(ax)

# --- Panel: censura ----------------------------------------------------------
ax = ejes[1, 0]
ax.hist(registrado, bins=70, range=(0, 20), color=NARANJA)
ax.axvline(tope, color=ROJO, linewidth=1.6)
ax.set_xlim(0, 20)
ax.set_xlabel("tiempo de espera registrado (minutos)")
ax.set_ylabel("casos")
anotar(ax, f"el proceso corta en {tope:.0f}", (tope, 2900), (0.94, 0.90), color=ROJO, align="right")
anotar(ax, f"un solo valor posible: {censurado:.1f} % de los casos", (tope, 3300), (0.94, 0.70),
       color=TEXTO, align="right")
titulo(ax, "La censura apila la cola en el limite", "los casos largos ya no se distinguen")
numeros(ax)
rejilla(ax)

# --- Panel: ceros de mas -----------------------------------------------------
ax = ejes[1, 1]
cuenta = np.bincount(visitas, minlength=11)[:11]
ax.bar(range(11), cuenta, color=CIAN, width=0.7)
ax.set_xlabel("visitas en la semana")
ax.set_ylabel("usuarios")
ax.set_xticks(range(11))
ax.set_ylim(0, 8000)
anotar(ax, f"{sin_visita:.1f} % no visita ninguna vez", (0, cuenta[0]), (0.18, 0.90), color=TEXTO)
anotar(ax, "los que visitan siguen otro proceso", (5, cuenta[5]), (0.60, 0.50), color=VERDE)
titulo(ax, "El cero es otro fenomeno, no un valor bajo", "dos decisiones mezcladas en una columna")
numeros(ax, ejes="y")
rejilla(ax)

fig.suptitle("Cuatro formas de no parecerse a una campana", fontsize=11.5)
guardar(fig, "distribuciones-reales-cuatro-patrones")
