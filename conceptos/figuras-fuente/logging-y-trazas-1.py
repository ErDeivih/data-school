"""logging-y-trazas-1.py — lo que cuesta registrar y lo que arregla muestrear. La figura de la
pagina de registro y trazas (fase 11)."""

import numpy as np

from comun import *

estilo()

# Los numeros del ejemplo de la pagina: 200 peticiones por segundo, lineas de 250 bytes.
rps, bytes_por_linea = 200, 250


def por_dia(lineas_por_peticion):
    """Bytes al dia de una configuración: se escribe, se transporta, se indexa y se guarda."""
    return rps * lineas_por_peticion * bytes_por_linea * 86400


# Tres formas de registrar la misma peticion: apagado, el nivel de informacion y el de depuracion.
configuraciones = ["sin registro", "INFO\n3 lineas", "DEBUG\n40 lineas"]
gb_dia = np.array([0.0, por_dia(3) / 1e9, por_dia(40) / 1e9])
colores = [VERDE, AZUL, ROJO]

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.6, 4.2))

# --- Izquierda: el volumen diario de cada nivel -------------------------------------
barras = izq.bar(configuraciones, gb_dia, color=colores, width=0.55)
izq.bar_label(barras, labels=[f"{v:.1f}".replace(".", ",") for v in gb_dia], padding=3, fontsize=9)
# La raya del nivel de informacion deja ver de un golpe que depurar multiplica por trece.
izq.axhline(gb_dia[1], color=REJILLA, linewidth=1.0, linestyle="--")
izq.text(2.42, gb_dia[1] + 4, "lo que cuesta INFO", color=REJILLA, fontsize=8.5, ha="right")
# La comparacion de las dos lineas es la frase que hay que llevarse: 40 / 3 = 13.
anotar(izq, "trece veces más por\nla misma petición", xy=(2, gb_dia[2]), xytext=(0.30, 0.76),
       color=ROJO)
izq.set_ylim(0, 210)
izq.set_ylabel("GB al dia")
titulo(izq, "Depurar en producción multiplica por trece",
       "200 peticiones por segundo, lineas de 250 bytes")
rejilla(izq)
numeros(izq, ejes="y")

# --- Derecha: apagar no es la unica salida, muestrear si ----------------------------
# De las 40 lineas de depuracion, 2 son de un caso interesante (error o peticion lenta) y 38
# son el detalle rutinario. Se guarda el 100 % de lo interesante y una decima parte del resto.
interesantes, rutinarias = 2, 38
lineas_muestreadas = interesantes + 0.1 * rutinarias
gb_muestreo = por_dia(lineas_muestreadas) / 1e9
opciones = ["todo el detalle\n(DEBUG)", "errores enteros\ny 10 % del resto"]
valores = np.array([gb_dia[2], gb_muestreo])
barras2 = der.bar(opciones, valores, color=[ROJO, VERDE], width=0.45)
der.bar_label(barras2, labels=[f"{v:.1f} GB".replace(".", ",") for v in valores], padding=3,
              fontsize=9)
anotar(der, "el detalle de un caso\nraro sigue estando", xy=(1, gb_muestreo), xytext=(0.45, 0.64),
       color=VERDE)
der.set_ylim(0, 210)
der.set_ylabel("GB al dia")
titulo(der, "Muestrear en vez de apagar",
       "todo el error y una fracción de lo que sale bien")
rejilla(der)
numeros(der, ejes="y")

guardar(fig, "logging-volumen-y-muestreo")
