"""asimetria-y-curtosis-1.py — el sesgo dice hacia donde tira la cola; la curtosis, cuanto pesa.

Arriba, dos nubes estandarizadas (media 0 y desviación 1) contra la campana de Gauss de
referencia: los dientes que sobresalen de la curva por los lados son el peso de la cola, que es
lo que mide la curtosis. Abajo, las tres nubes enteras vistas de lejos y con la altura en escala
logaritmica: así se ven los dos dias de panico que en el primer plano no caben.
"""

import numpy as np
from scipy import stats

from comun import *

estilo()

azar = np.random.default_rng(7)
normal = azar.normal(0.0, 1.0, 4000)
# Salarios, precios y tiempos de espera: muchos valores bajos y unos pocos altisimos. Con
# sigma = 0,5 la asimetria teorica es 1,75 y la curtosis 5,9, que es lo que se ve en los datos.
lognormal = azar.lognormal(mean=0.0, sigma=0.5, size=4000)
# Dias de calma y dos desplomes del 4 %: la asimetria negativa de los retornos reales.
retornos = np.concatenate([azar.normal(0.15, 0.30, 3998), [-4.0, -4.5]])


def estandarizar(datos):
    return (datos - datos.mean()) / datos.std(ddof=1)


def resumen(z):
    return float(stats.skew(z, bias=False)), float(stats.kurtosis(z, bias=False))


z_normal = estandarizar(normal)
z_lognormal = estandarizar(lognormal)
z_retornos = estandarizar(retornos)
g1_normal, g2_normal = resumen(z_normal)
g1_lognormal, g2_lognormal = resumen(z_lognormal)
g1_retornos, g2_retornos = resumen(z_retornos)

fig = plt.figure(figsize=(10.6, 7.0))
rejilla_paneles = fig.add_gridspec(2, 2)
arriba_izq = fig.add_subplot(rejilla_paneles[0, 0])
arriba_der = fig.add_subplot(rejilla_paneles[0, 1])
abajo = fig.add_subplot(rejilla_paneles[1, :])

central = np.arange(-5.0, 5.01, 0.1)
campana = stats.norm.pdf(central)

for eje, z, color, titulo_corto in (
        (arriba_izq, z_normal, AZUL, "Normal: la nube sigue la campana"),
        (arriba_der, z_lognormal, NARANJA, "Cola a la derecha: la nube se sale")):
    eje.bar(central, np.histogram(z, bins=np.append(central - 0.05, central[-1] + 0.05))[0],
            width=0.095, color=color, alpha=0.70, label="los datos, estandarizados")
    eje.plot(central, campana * z.size * 0.1, color=TEXTO, linewidth=1.5,
             label="la normal con esa misma media y desviaci\u00f3n")
    eje.set_xlim(-5, 5)
    eje.set_ylim(0, 350)
    eje.set_xlabel("valor estandarizado (z)")
    eje.set_ylabel("n\u00famero de valores")
    titulo(eje, titulo_corto)
    numeros(eje)
    rejilla(eje)

arriba_der.legend(loc="upper left", fontsize=8.5)
arriba_der.annotate("aqu\u00ed la curva ya casi no llega",
                    xy=(4.3, 14), xycoords="data", xytext=(0.50, 0.30),
                    textcoords="axes fraction", fontsize=8.5, color=NARANJA, va="center",
                    arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=0.9, shrinkA=2,
                                    shrinkB=4))

# Los tres resumenes van encima de su propia franja, mas abajo.

# --- Abajo: las tres nubes enteras ----------------------------------------------------------
# Cada franja se dibuja en su propio maximo (de 0 a 1): asi la masa central no aplasta al
# valor unico de la cola, que es lo que se quiere ver. Con la altura en bruto, dos valores de
# 4.000 tapan todo lo demas y la cola desaparece.
# Los resumenes (asimetria y curtosis) van justo encima de su franja: dentro de los paneles de
# arriba se cruzaban con las barras o con la leyenda.
bordes = np.arange(-17.0, 17.01, 0.1)
filas = [(2.0, z_normal, AZUL, g1_normal, g2_normal, "normal"),
         (1.0, z_lognormal, NARANJA, g1_lognormal, g2_lognormal, "cola a la derecha"),
         (0.0, z_retornos, ROJO, g1_retornos, g2_retornos, "dos d\u00edas de p\u00e1nico")]
for y, z, color, g1, g2, nombre in filas:
    recuentos, _ = np.histogram(z, bins=bordes)
    # La franja es horizontal: barh pone el grosor en `height` y la longitud en `width`.
    abajo.barh(np.full(recuentos.size, y), np.maximum(recuentos, 1.0) / recuentos.max(),
               height=0.55, left=bordes[:-1], align="edge", color=color)
    abajo.text(-16.9, y, nombre, color=color, fontsize=9, va="center")
    abajo.text(-0.4, y + 0.80, "asimetr\u00eda %+.2f   curtosis en exceso %+.2f" % (g1, g2),
               color=color, fontsize=8.5, ha="left", va="center")
abajo.axvline(0, color=TEXTO, linewidth=0.9)
abajo.set_xlim(-17, 17)
abajo.set_ylim(-0.35, 3.65)
abajo.set_yticks([])
abajo.set_xticks([-17, -15, -11, -7, -3, -1, 0, 1, 3, 7, 11, 15, 17])

abajo.annotate("aqu\u00ed est\u00e1n los dos d\u00edas de p\u00e1nico",
               xy=(-8.95, 0.28), xycoords="data", xytext=(0.16, 0.12),
               textcoords="axes fraction", fontsize=8.5, color=ROJO, va="center",
               arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=2,
                               shrinkB=4))
abajo.annotate("el valor m\u00e1s alto de los ingresos",
               xy=(7.6, 1.28), xycoords="data", xytext=(0.62, 0.44),
               textcoords="axes fraction", fontsize=8.5, color=NARANJA, va="center",
               arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=0.9, shrinkA=2,
                               shrinkB=4))

titulo(abajo, "Vistas enteras, las tres tienen la misma media y la misma desviaci\u00f3n",
       "cada franja llega a su propio m\u00e1ximo (0 a 1): as\u00ed se ven los valores \u00fanicos que la masa central esconde")
abajo.set_xlabel("valor estandarizado (z)")

guardar(fig, "asimetria-y-curtosis-misma-media-distinta-forma")
