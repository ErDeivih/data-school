"""var-y-cvar-1.py — el VaR marca el umbral y el CVaR dice cuánto hay detrás: dos carteras con
exactamente el mismo VaR al 95 % pueden tener colas que no se parecen en nada. Figura de la
página de VaR y CVaR (fase 9)."""

import numpy as np

from comun import *


def pct(x, decimales=2):
    """Porcentaje con coma decimal, como se escribe en el portal."""
    return f"{x * 100:.{decimales}f} %".replace(".", ",")


def suavizar(y, k=7):
    """Media móvil de k puntos: la densidad empírica de la cola sale a saltos y así se lee
    como una curva."""
    return np.convolve(y, np.ones(k) / k, mode="same")


def var_cvar(perdidas, probs, cola=0.05):
    """VaR y CVaR coherente de una distribución discreta: el CVaR es la media del peor `cola`,
    repartiendo la masa del escalón que cae justo en el umbral."""
    orden = np.argsort(-perdidas)
    pe, pr = perdidas[orden], probs[orden]
    var = float(pe[np.searchsorted(np.cumsum(pr), cola)])
    resto, cvar = cola, 0.0
    for perdida_i, peso in zip(pe, pr):
        toma = min(peso, resto)
        cvar += toma * perdida_i
        resto -= toma
    return var, cvar / cola


estilo()
azar = np.random.default_rng(7)

# --- Izquierda: dos carteras con el MISMO VaR al 95 % y colas incomparables.
# La azul supone retornos normales; la naranja tiene colas gruesas (t de Student con 3 grados),
# que es lo que de verdad se ve en series financieras.
n = 400_000
perdida_normal = -azar.normal(0.0, 0.012, n)          # la pérdida es el retorno con el signo cambiado
perdida_t = -azar.standard_t(3, n)

# Se reescala la t para que su cuantil 95 % caiga justo donde el de la normal: así las dos
# carteras tienen el mismo VaR y todo lo que se vea de diferencia es cola, no umbral.
var = float(np.quantile(perdida_normal, 0.95))
perdida_gruesa = perdida_t * (var / float(np.quantile(perdida_t, 0.95)))
# El CVaR es la media de todo lo que queda por encima del umbral: el 5 % de los peores días.
cvar_normal = float(perdida_normal[perdida_normal >= var].mean())
cvar_gruesa = float(perdida_gruesa[perdida_gruesa >= var].mean())

bordes = np.linspace(-0.06, 0.095, 150)
centros = 0.5 * (bordes[:-1] + bordes[1:])
dens_normal = suavizar(np.histogram(perdida_normal, bins=bordes, density=True)[0])
dens_gruesa = suavizar(np.histogram(perdida_gruesa, bins=bordes, density=True)[0])

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))

ejes[0].plot(centros, dens_normal, color=AZUL, linewidth=2.0, label="retornos normales")
ejes[0].fill_between(centros, dens_normal, where=centros >= var, color=AZUL, alpha=0.30)
ejes[0].plot(centros, dens_gruesa, color=NARANJA, linewidth=2.0, label="colas gruesas (t de Student)")
ejes[0].fill_between(centros, dens_gruesa, where=centros >= var, color=NARANJA, alpha=0.30)
ejes[0].axvline(var, color=ROJO, linewidth=1.4, linestyle="--")
# Los dos CVaR se marcan sobre el eje para poder compararlos de un vistazo: están a 8 puntos
# básicos de distancia, pero uno es un 25 % más alto que el otro.
ejes[0].plot([cvar_normal], [0], marker="o", markersize=8, color=AZUL, clip_on=False)
ejes[0].plot([cvar_gruesa], [0], marker="o", markersize=8, color=NARANJA, clip_on=False)
anotar(ejes[0], f"el umbral: VaR al 95 % = {pct(var)}\nsolo lo supera uno de cada veinte días",
       xy=(var, float(np.interp(var, centros, dens_gruesa))), xytext=(0.03, 0.80), color=ROJO)
anotar(ejes[0], f"la cola de la t: CVaR {pct(cvar_gruesa)}",
       xy=(cvar_gruesa, 0.0), xytext=(0.98, 0.38), color=NARANJA, align="right")
anotar(ejes[0], f"la cola normal: CVaR {pct(cvar_normal)}",
       xy=(cvar_normal, 0.0), xytext=(0.98, 0.18), color=AZUL, align="right")
titulo(ejes[0], "El VaR no distingue estas dos colas",
       "misma pérdida en el percentil 95, muy distinta pérdida media en el 5 % peor")
ejes[0].set_xlabel("pérdida del día, en tanto por uno del capital")
ejes[0].set_ylabel("densidad de los días")
ejes[0].set_xlim(-0.055, 0.095)
# El margen de arriba se calcula con la densidad más alta de las dos: la cola gruesa tiene el
# pico más alto y, si se deja el margen de la normal, el título y la leyenda caen encima.
ejes[0].set_ylim(0, float(max(dens_normal.max(), dens_gruesa.max())) * 1.60)
ejes[0].legend(loc="upper right", fontsize=8)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: el ejemplo de los dos bonos. La suma de los VaR de las partes no acota el VaR
# del conjunto, y ahí se rompe la coherencia de la medida.
p, perdida = 0.04, 100.0
un_bono = var_cvar(np.array([0.0, perdida]), np.array([1 - p, p]))
dos_bonos = var_cvar(np.array([0.0, perdida, 2 * perdida]),
                     np.array([(1 - p) ** 2, 2 * p * (1 - p), p ** 2]))
partes = [2 * un_bono[0], 2 * un_bono[1]]
junta = [dos_bonos[0], dos_bonos[1]]

posiciones = np.arange(4)
# En barras horizontales el orden se lee de abajo arriba: primero el VaR, después el CVaR.
valores = [partes[0], junta[0], partes[1], junta[1]]
colores = [MORADO, CIAN, MORADO, CIAN]
ejes[1].barh(posiciones, valores, height=0.55, color=colores, alpha=0.85, zorder=2)
for yi, valor in zip(posiciones, valores):
    ejes[1].text(valor + 8, yi, f"{valor:.0f} €", va="center", fontsize=9,
                 color=MORADO if yi in (0, 2) else CIAN, zorder=3)
ejes[1].set_yticks(posiciones)
ejes[1].set_yticklabels(["VaR · las dos sueltas", "VaR · la cartera",
                         "CVaR · las dos sueltas", "CVaR · la cartera"], fontsize=9)
ejes[1].set_xlim(0, 430)
ejes[1].set_ylim(-0.65, 3.65)
anotar(ejes[1], "0 € < 100 €: el VaR de la cartera supera\nla suma de los VaR sueltos",
       xy=(40.0, 1.0), xytext=(0.36, 0.44), color=ROJO)
anotar(ejes[1], "160 € > 103 €: el CVaR de la cartera\nqueda por debajo de la suma",
       xy=(40.0, 2.55), xytext=(0.52, 0.88), color=VERDE)
titulo(ejes[1], "El VaR castiga diversificar; el CVaR no",
       "dos bonos con un 4 % de impago cada uno, de 100 € y con impagos independientes")
ejes[1].set_xlabel("pérdida, en euros")
rejilla(ejes[1], eje="x")
numeros(ejes[1], ejes="x")

guardar(fig, "var-y-cvar-umbral-y-cola")
