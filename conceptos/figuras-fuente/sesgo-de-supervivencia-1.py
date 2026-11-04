"""sesgo-de-supervivencia-1.py — quien desaparece de la muestra no desaparece al azar:
desaparece el que iba mal, y la media que queda no es la del sector. La figura de la pagina
del sesgo de supervivencia (fase 9)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)
n = 900
# Dos periodos de rentabilidad, uno detras de otro: sirven para ver quien se cae de la muestra.
r1 = azar.normal(0.02, 0.12, n)
r2 = azar.normal(0.02, 0.12, n)
resultado = (r1 + r2) / 2

# La probabilidad de seguir en la base de datos depende del rango que ocupas: al mejor lo
# conservan, al peor lo borran. Quedarse con el 60 % de arriba es lo que hace una consulta
# del tipo "fondos con diez años de historial".
rango = resultado.argsort().argsort() / (n - 1)
vive = rango >= 0.40

fig, ejes = plt.subplots(1, 2, figsize=(7.6, 3.9))

# --- Izquierda: quien se cae y por que la media de la muestra viva esta sesgada ---
ejes[0].axvspan(-0.45, 0, color=ROJO, alpha=0.06, linewidth=0)
ejes[0].scatter(r1[vive], r2[vive], s=9, color=VERDE, alpha=0.5, linewidths=0)
ejes[0].scatter(r1[~vive], r2[~vive], s=12, color=ROJO, alpha=0.55, linewidths=0)
ejes[0].axvline(0, color=NARANJA, linewidth=1.1, linestyle="--")
ejes[0].axhline(0, color=NARANJA, linewidth=1.1, linestyle="--")
ejes[0].set_title("Los que desaparecen no desaparecen al azar")
ejes[0].set_xlabel("rentabilidad del primer periodo")
ejes[0].set_ylabel("rentabilidad del segundo")
for grupo, color, etiqueta, pos in ((np.ones(n, bool), REJILLA, "cohorte entera", 0.02),
                                    (vive, VERDE, "los que siguen vivos", 0.09)):
    pendiente, corte = np.polyfit(r1[grupo], r2[grupo], 1)
    xs = np.array([r1.min(), r1.max()])
    ejes[0].plot(xs, pendiente * xs + corte, color=color, linewidth=1.5,
                 linestyle="--" if color == REJILLA else "-")
    ejes[0].text(0.98, pos, "media de la %s: %+.1f %%" % (etiqueta, 100 * resultado[grupo].mean()),
                 color=color, fontsize=8.5, ha="right", va="bottom", transform=ejes[0].transAxes)
ejes[0].annotate("los que cerraron\nsolo están aquí", xy=(-0.28, -0.25), xytext=(0.05, 0.20),
                 textcoords="axes fraction", fontsize=8.5, color=ROJO,
                 arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9))
rejilla(ejes[0], "both")
numeros(ejes[0])

# --- Derecha: cuanto mas selectiva es la muestra, mas se infla la media ---
# Se varia el corte de supervivencia y se mide el sesgo resultante, que es lo unico que cambia.
cortes = np.linspace(0.0, 0.95, 60)
fraccion, desvio = [], []
for corte in cortes:
    vivos = rango >= corte
    if vivos.sum() > 20:
        fraccion.append(float(vivos.mean()))
        desvio.append(float(resultado[vivos].mean() - resultado.mean()))
ejes[1].plot(fraccion, desvio, color=MORADO, linewidth=1.9)
ejes[1].axhline(0, color=TEXTO, linewidth=0.8, alpha=0.4)
ejes[1].set_title("Cuanta menos muestra queda, más se infla la media")
ejes[1].set_xlabel("fracción de la cohorte que sigue viva")
ejes[1].set_ylabel("sesgo de la media (pp)")
ejes[1].text(0.97, 0.06, "si no desapareciera nadie,\nel sesgo sería exactamente cero",
             color=REJILLA, fontsize=8.5, ha="right", transform=ejes[1].transAxes)
mitad = int(0.30 * len(desvio))
ejes[1].annotate("quedarse con la mitad mejor\nya inventa %+.1f pp al año" % desvio[mitad],
                 xy=(fraccion[mitad], desvio[mitad]),
                 xytext=(0.06, 0.80), textcoords="axes fraction", fontsize=8.5, color=NARANJA,
                 arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=0.9))
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "sesgo-de-supervivencia-los-que-faltan")
