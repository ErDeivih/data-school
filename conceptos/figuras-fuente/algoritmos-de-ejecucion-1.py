"""algoritmos-de-ejecucion-1.py — el perfil de volumen intradía es una U: la primera y la última
hora concentran la mayor parte del volumen. TWAP reparte el pedido a partes iguales y VWAP lo
reparte siguiendo ese perfil. Página de Algoritmos de ejecución (fase 9)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

MINUTOS = 390                      # de 09:30 a 16:00, seis horas y media de negociación continua
t = np.arange(MINUTOS)
# Perfil en U: mucho al abrir (subasta y noticias de la noche), valle a mediodía y repunte al
# cerrar, donde además se acumulan las órdenes de la subasta de cierre.
perfil = 0.60 + 2.60 * ((t - MINUTOS / 2) / (MINUTOS / 2)) ** 2
perfil *= 1.0 + 0.06 * azar.standard_normal(MINUTOS)      # ruido del día; la forma es la de siempre
perfil = np.clip(perfil, 0.05, None)
volumen = perfil / perfil.sum()                           # fracción del volumen diario por minuto

TROZOS = 39                        # un tramo cada diez minutos, como haría un bróker de verdad
bordes = np.linspace(0, MINUTOS, TROZOS + 1).astype(int)
peso_por_tramo = np.array([volumen[a:b].sum() for a, b in zip(bordes[:-1], bordes[1:])])
centro = [(a + b) // 2 for a, b in zip(bordes[:-1], bordes[1:])]

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

# --- Izquierda: la forma del volumen y cómo se colocan los dos algoritmos.
ejes[0].fill_between(t, 0, volumen * 100, color=CIAN, alpha=0.18, linewidth=0)
ejes[0].plot(t, volumen * 100, color=CIAN, linewidth=1.8, label="volumen por minuto")
paso_twap = 100.0 / TROZOS
ejes[0].plot([0, MINUTOS - 1], [paso_twap, paso_twap], color=MORADO, linewidth=2.0,
             linestyle="--", label=f"rodaja TWAP: {paso_twap:.2f} % cada 10 min")
ejes[0].scatter(centro, peso_por_tramo * 100, color=ROJO, s=22, zorder=5,
                label="rodaja VWAP: según el volumen")
anotar(ejes[0], "el cierre concentra casi una décima\nparte del volumen del día",
       xy=(float(t[-1]), float(volumen[-1] * 100)), xytext=(0.42, 0.82), color=CIAN)
titulo(ejes[0], "El volumen intradía tiene forma de U",
       "y cada algoritmo reparte el pedido según esa forma")
ejes[0].set_xlabel("minutos desde la apertura")
ejes[0].set_ylabel("porcentaje del volumen diario")
# La leyenda lleva fondo blanco: cruza la línea de puntos del ritmo TWAP y sin él el texto
# se lee fatal. Es la única caja del tema que no sale de una variable CSS, a propósito.
leyenda = ejes[0].legend(loc="lower right", fontsize=7.0, frameon=True)
leyenda.get_frame().set_facecolor("white")
leyenda.get_frame().set_edgecolor("none")
rejilla(ejes[0])

# --- Derecha: ejecución acumulada. Una diagonal perfecta es TWAP; la escalera es VWAP, que
# adelanta pedido en la apertura y lo vuelve a cargar al final.
acum_twap = np.array([paso_twap * (i + 1) for i in range(TROZOS)])
acum_vwap = 100 * np.cumsum(peso_por_tramo)
ejes[1].plot(centro, acum_twap, color=MORADO, linewidth=2.0, linestyle="--",
             label="TWAP: ritmo constante")
ejes[1].plot(centro, acum_vwap, color=ROJO, linewidth=2.0,
             label="VWAP: se pega al volumen del mercado")
ejes[1].fill_between(centro, acum_twap, acum_vwap, color=ROJO, alpha=0.12, linewidth=0)
desvio = float(np.abs(acum_vwap - acum_twap).max())
anotar(ejes[1], f"la mayor separación entre los dos\nritmos es {desvio:.1f} puntos del pedido",
       xy=(float(centro[int(np.argmax(np.abs(acum_vwap - acum_twap)))]),
           float(acum_vwap[int(np.argmax(np.abs(acum_vwap - acum_twap)))])),
       xytext=(0.05, 0.86), color=ROJO)
titulo(ejes[1], "Cuánto llevas ejecutado a cada hora",
       "la curva de VWAP es el volumen acumulado; la de TWAP, una recta")
ejes[1].set_xlabel("minutos desde la apertura")
ejes[1].set_ylabel("pedido ejecutado (porcentaje)")
ejes[1].legend(loc="lower right", fontsize=8)
rejilla(ejes[1])
numeros(ejes[1], ejes="y")

guardar(fig, "algoritmos-de-ejecucion-perfil-y-ritmo")
