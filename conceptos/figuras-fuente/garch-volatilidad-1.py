"""garch-volatilidad-1.py — la volatilidad se agrupa y se puede pronosticar.

El hecho del que nace el modelo: el signo del retorno no se correlaciona con el de ayer, pero su
magnitud si. Y la consecuencia: la volatilidad sube con los sustos y tarda semanas en volver a su
nivel. La figura de la pagina de GARCH y volatilidad (fase 5)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# Un GARCH(1,1) con la persistencia tipica de un indice de bolsa: alfa + beta = 0,98
omega, alpha, beta = 1e-5, 0.20, 0.78
larga = omega / (1 - alpha - beta)          # varianza incondicional: 0,0005 -> 2,24% diario
n = 900
z = azar.standard_normal(n)
eps = np.zeros(n)
var = np.empty(n)
var[0] = larga
for t in range(1, n):                       # la varianza de hoy mira el susto y la varianza de ayer
    var[t] = omega + alpha * eps[t - 1] ** 2 + beta * var[t - 1]
    eps[t] = np.sqrt(var[t]) * z[t]
vol = np.sqrt(var)
absoluto = np.abs(eps)

corr_signo = np.corrcoef(eps[1:], eps[:-1])[0, 1]
corr_magnitud = np.corrcoef(absoluto[1:], absoluto[:-1])[0, 1]
retardos = np.arange(1, 13)
acf_abs = np.array([np.corrcoef(absoluto[k:], absoluto[:-k])[0, 1] for k in retardos])

fig = plt.figure(figsize=(11.0, 6.4))
rej = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.65], hspace=0.55, wspace=0.28)
ax_nube = fig.add_subplot(rej[0, 0])
ax_acf = fig.add_subplot(rej[1, 0])
ax_vol = fig.add_subplot(rej[:, 1])

# --- Panel 1: el signo de ayer no dice nada, el tamaño si ---------------------
ax_nube.scatter(absoluto[:-1] * 100, absoluto[1:] * 100, s=5, color=AZUL, alpha=0.35,
                edgecolors="none")
ax_nube.set_title("Lo que se puede predecir no es el signo")
ax_nube.set_xlabel("magnitud del retorno de ayer, en %")
ax_nube.set_ylabel("magnitud del retorno de hoy, en %")
ax_nube.set_xlim(0, 6.5)
ax_nube.set_ylim(0, 6.5)
rejilla(ax_nube)
numeros(ax_nube)
ax_nube.text(0.05, 0.92, "correlación de los signos: %.2f\ncorrelación de las magnitudes: %.2f"
             % (corr_signo, corr_magnitud), transform=ax_nube.transAxes, fontsize=8.5, color=TEXTO)
ax_nube.text(0.05, 0.05, "la nube se abre hacia arriba a la derecha:\ntras un dia grande viene otro dia grande",
             transform=ax_nube.transAxes, fontsize=8.5, color=MORADO)

# --- Panel 2: esa dependencia dura semanas, no un dia -------------------------
ax_acf.bar(retardos, acf_abs, color=VERDE, width=0.62)
ax_acf.axhline(0, color=TEXTO, linewidth=0.8)
ax_acf.axhline(2 / np.sqrt(n), color=ROJO, linewidth=1.0, linestyle="--")
ax_acf.set_title("Y dura semanas, no un dia")
ax_acf.set_xlabel("retardos, en dias")
ax_acf.set_ylabel("autocorrelación de la magnitud")
rejilla(ax_acf)
numeros(ax_acf)
ax_acf.text(0.30, 0.95, "la banda roja es el ruido:\nlo que sobresale es memoria",
            transform=ax_acf.transAxes, fontsize=8.5, color=ROJO)

# --- Panel 3: la volatilidad, su nivel y lo que tarda en volver ---------------
ax_vol.plot(vol * 100, color=AZUL, linewidth=1.5)
nivel = 100 * np.sqrt(larga)
ax_vol.axhline(nivel, color=VERDE, linewidth=1.4, linestyle="--")
ax_vol.fill_between(np.arange(n), nivel, vol * 100, where=vol * 100 > nivel,
                    color=ROJO, alpha=0.18, interpolate=True)
ax_vol.set_ylim(0, vol.max() * 100 * 1.16)
ax_vol.set_title("La volatilidad condicional que el modelo ve venir")
ax_vol.set_xlabel("dia")
ax_vol.set_ylabel("volatilidad diaria, en %")
rejilla(ax_vol)
numeros(ax_vol)
racha = int(np.argmax(vol[100:]) + 100)
anotar(ax_vol, "un susto la dispara y tarda 34 dias en irse a la mitad,\nporque alfa + beta = 0,98",
      xy=(racha, vol[racha] * 100), xytext=(0.03, 0.92), color=ROJO)
anotar(ax_vol, "el nivel al que siempre vuelve: 2,24% diario",
      xy=(n * 0.72, nivel), xytext=(0.42, 0.62), color=VERDE)
ax_vol.text(0.03, 0.05, "la zona sombreada es el exceso de volatilidad: en ella toca reducir\nel tamaño de la posición, no adivinar hacia donde va el precio",
            transform=ax_vol.transAxes, fontsize=8.5, color=MORADO)

guardar(fig, "garch-volatilidad-se-agrupa-y-vuelve")
