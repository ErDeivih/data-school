"""inferencia-propia-1.py — qué cuesta servir tus propios tokens, contra qué precio de API sale
a cuenta y por qué los picos se llevan la mayor parte de la factura. La figura de la página de
economía de la inferencia propia."""

import numpy as np

from comun import *

estilo()

# Parámetros de trabajo. Todo lo que afirma la página sale de aquí.
PRECIO_GPU_HORA = 2.50           # euros por GPU y hora, alquiler bajo demanda
TOKENS_POR_SEGUNDO = 2000.0      # tokens de salida por segundo con un lote razonable
DIAS_MES = 30
TOKENS_MES_GPU = TOKENS_POR_SEGUNDO * 3600 * 24 * DIAS_MES / 1e6   # millones al 100 %
COSTE_GPU_MES = PRECIO_GPU_HORA * 24 * DIAS_MES
COSTE_LLENO = COSTE_GPU_MES / TOKENS_MES_GPU                      # EUR por millón al 100 %


def coste_por_millon(utilizacion):
    """Euros por millón de tokens servidos a esa utilización (fracción de la capacidad)."""
    return COSTE_LLENO / utilizacion


# Escenario: 20 millones de tokens al día de media, con picos diez veces la media. Si se
# dimensiona para el pico, la utilización media es exactamente 1 / 10.
MEDIA_DIARIA = 20.0                       # millones de tokens al día
MEDIA_MES = MEDIA_DIARIA * DIAS_MES       # millones al mes
PICO_SOBRE_MEDIA = 10.0
GPUS = MEDIA_MES / TOKENS_MES_GPU * PICO_SOBRE_MEDIA
utilizacion_media = MEDIA_MES / (TOKENS_MES_GPU * GPUS)

# Precios de referencia de una API por millón de tokens de salida.
PRECIOS_API = [0.10, 0.50, 1.00, 3.00, 15.00]
equilibrios = [p / COSTE_LLENO * 100 for p in PRECIOS_API]

fig, ejes = plt.subplots(2, 1, figsize=(8.6, 7.6))

# --- Arriba: la curva de coste y dónde cae una carga con picos -----------------
u = np.linspace(0.03, 1.0, 400)
ejes[0].plot(u * 100, [coste_por_millon(x) for x in u], color=AZUL, linewidth=1.8)
y_carga = coste_por_millon(utilizacion_media)
ejes[0].plot([utilizacion_media * 100], [y_carga], marker="o", markersize=6, color=ROJO)
anotar(ejes[0], f"dimensionando para el pico\nde {PICO_SOBRE_MEDIA:.0f} veces la media"
                f" queda en {utilizacion_media:.0%}",
       xy=(utilizacion_media * 100, y_carga), xytext=(0.20, 0.70), color=ROJO)
for p, color in ((0.50, VERDE), (3.00, MORADO), (15.00, NARANJA)):
    ejes[0].axhline(p, color=color, linewidth=1.2, linestyle="--")
    ejes[0].text(98, p, f"API a {p:.2f} EUR/M", ha="right", va="bottom", fontsize=8, color=color)
ejes[0].set_yscale("log")
ejes[0].set_xlabel("utilización de la capacidad que has comprado (%)")
ejes[0].set_ylabel("euros por millón de tokens")
titulo(ejes[0], "El precio por token lo decide la utilización",
       "el alquiler de la GPU se paga entero; los tokens que salen de ella, no")
rejilla(ejes[0], "both")
numeros(ejes[0], "x")

# --- Abajo: utilización de equilibrio frente a cada precio de API --------------
# Por encima del 100 % no hay equilibrio posible: ni con la GPU a pleno rendimiento.
barras = ejes[1].barh([f"{p:.2f}" for p in PRECIOS_API], equilibrios,
                      color=[VERDE, CIAN, AZUL, MORADO, NARANJA], height=0.6)
for barra, v in zip(barras, equilibrios):
    dentro = v < 200
    ejes[1].text(v * (0.5 if dentro else 1.06), barra.get_y() + barra.get_height() / 2,
                 f"{v:.1f} %", va="center", ha="center" if dentro else "left",
                 fontsize=8.5, color="white" if dentro else TEXTO)
# La raya del 100 % va a la leyenda y no como texto suelto: arriba choca con el subtítulo y
# abajo, con las etiquetas de las barras. La leyenda se coloca sola donde hay hueco.
ejes[1].axvline(100, color=ROJO, linewidth=1.4, linestyle="--",
                label="100 % = la GPU, sin parar")
ejes[1].set_xscale("log")
ejes[1].set_xlim(5, 20000)
ejes[1].set_xlabel("utilización que necesitas para igualar el precio de la API (%, escala log)")
ejes[1].set_ylabel("precio de la API (EUR por millón)")
titulo(ejes[1], "Solo se baten las APIs caras, o con mucha carga",
       "cuanto más barata es la API, más tiempo tiene que estar ocupada tu GPU")
rejilla(ejes[1], "x")
numeros(ejes[1], "x")
ejes[1].legend(loc="lower right", fontsize=8)

guardar(fig, "inferencia-propia-utilizacion-y-equilibrio")

print("millones de tokens al mes que da una GPU al 100 %", round(TOKENS_MES_GPU, 1))
print("coste de una GPU al mes", round(COSTE_GPU_MES, 2), "EUR")
print("coste por millon al 100 % de utilización", round(COSTE_LLENO, 4), "EUR")
print("GPUs que hay que tener para el pico", round(GPUS, 3))
print("utilización media", f"{utilizacion_media:.4%}")
print("coste por millon que sale de ahi", round(y_carga, 4), "EUR")
print("factura mensual del propio", round(COSTE_GPU_MES * max(1, int(np.ceil(GPUS))), 2), "EUR")
print("factura mensual con el pico dimensionado al pico exacto",
      round(COSTE_GPU_MES * GPUS, 2), "EUR")
for x in (0.05, 0.10, 0.20, 0.30, 0.60, 1.00):
    print(f"  utilización {x:5.0%} -> {coste_por_millon(x):7.4f} EUR por millon")
print("equilibrio frente a cada API", [f"{p:.2f}->{e:.1f}%" for p, e in zip(PRECIOS_API, equilibrios)])
for p in PRECIOS_API:
    print(f"  API {p:6.2f} EUR/M: factura de {MEDIA_MES} M al mes = {MEDIA_MES * p:,.0f} EUR"
          f"  frente a {COSTE_GPU_MES * max(1, int(np.ceil(GPUS))):,.0f} EUR del propio")
# Palanca de la cuantización: el mismo hardware sirve más tokens por segundo.
for factor, etiqueta in ((1.0, "sin cuantizar"), (1.6, "cuantizado a int8"), (2.3, "cuantizado a int4")):
    tokens = TOKENS_MES_GPU * factor
    coste = COSTE_GPU_MES / tokens
    print(f"  {etiqueta:18s} {factor:4.1f}x tokens/segundo -> {coste:.4f} EUR por millon al 100 %")
