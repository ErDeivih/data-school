"""errores-tipo-i-ii-y-potencia-1.py — las dos distribuciones que se solapan (nula y
alternativa) con α y β, y la curva de potencia frente al tamaño de muestra. Ejemplo de la
página: σ = 8 mm y un descentrado que importa de 2 mm. Figura de la página de errores
tipo I y II."""

import numpy as np
from scipy import stats

from comun import *

estilo()

sigma, delta, alpha = 8.0, 2.0, 0.05
z_alfa = stats.norm.ppf(1 - alpha / 2)          # 1,96 para el 5 % bilateral
eje = np.linspace(-4.2, 5.4, 1200)
nulo = stats.norm.pdf(eje, 0, 1)
# Con n = 25 la alternativa se separa delta*raiz(n)/sigma = 1,25 errores tipicos
separacion = delta * np.sqrt(25) / sigma
alterna = stats.norm.pdf(eje, separacion, 1)
beta = stats.norm.cdf(z_alfa - separacion)

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.1))

# --- Izquierda: donde acaba el 5% de la nula y donde vive el efecto que no se detecta.
ejes[0].plot(eje, nulo, color=AZUL, linewidth=1.8, label="H₀: la máquina está centrada")
ejes[0].plot(eje, alterna, color=NARANJA, linewidth=1.8, label="H₁: descentrada 2 mm")
ejes[0].fill_between(eje, nulo, where=eje >= z_alfa, color=ROJO, alpha=0.28)
ejes[0].fill_between(eje, alterna, where=eje <= z_alfa, color=MORADO, alpha=0.16)
ejes[0].fill_between(eje, alterna, where=eje >= z_alfa, color=VERDE, alpha=0.35)
ejes[0].axvline(z_alfa, color=ROJO, linewidth=1.3, linestyle="--",
                label="el umbral de decisión, 1,96")
anotar(ejes[0], "β = 0,761:\nel efecto real\nque no se ve",
       xy=(-1.8, 0.06), xytext=(0.02, 0.24), color=MORADO)
anotar(ejes[0], "α = 0,05:\nfalsa alarma", xy=(2.05, 0.03), xytext=(0.80, 0.65), color=ROJO)
anotar(ejes[0], "potencia 0,239\n= 1 − β", xy=(2.6, 0.06), xytext=(0.80, 0.30), color=VERDE)
ejes[0].set_xlabel("desviación de la media muestral, en errores típicos")
ejes[0].set_ylabel("densidad")
ejes[0].set_ylim(0, 0.86)
ejes[0].legend(loc="upper left")
titulo(ejes[0], "Con n = 25 el detector apenas distingue",
       "α = 0,05, β = 0,761 y potencia = 1 − β = 0,239: la mayor parte del efecto no se ve")
rejilla(ejes[0])
numeros(ejes[0], ejes="x")

# --- Derecha: la potencia frente al tamaño de muestra, con la raiz de n de fondo.
piezas = np.arange(2, 320)
potencia = stats.norm.cdf(delta * np.sqrt(piezas) / sigma - z_alfa)
ejes[1].plot(piezas, potencia, color=AZUL, linewidth=1.8)
ejes[1].axhline(0.80, color=TEXTO, linewidth=1.0, linestyle=":")
ejes[1].axvline(126, color=ROJO, linewidth=1.1, linestyle="--")
ejes[1].plot([25], [stats.norm.cdf(delta * 5 / sigma - z_alfa)], "o", color=ROJO,
             markersize=7, zorder=3)
ejes[1].plot([126], [0.801], "o", color=VERDE, markersize=7, zorder=3)
anotar(ejes[1], "n = 25: potencia 0,239", xy=(25, 0.239), xytext=(0.12, 0.40), color=ROJO)
anotar(ejes[1], "n = 126: potencia 0,801", xy=(126, 0.801), xytext=(0.46, 0.62), color=VERDE)
ejes[1].text(0.30, 0.10, "la potencia sube con la raíz de n: duplicar la separación\n"
             "cuesta cuatro veces más piezas (y pasar del 80 % al 90 %, un 34 % más)",
             transform=ejes[1].transAxes, fontsize=8.5, color=TEXTO)
ejes[1].set_xlabel("piezas medidas (n)")
ejes[1].set_ylabel("potencia del contraste")
ejes[1].set_xlim(0, 330)
ejes[1].set_ylim(0, 1.05)
titulo(ejes[1], "La potencia crece con √n, no con n",
       "σ = 8 mm, efecto de 2 mm, α = 0,05 bilateral")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "potencia-solape-y-muestra-necesaria")
