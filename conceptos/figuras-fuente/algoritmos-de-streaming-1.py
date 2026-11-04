"""algoritmos-de-streaming-1.py — el error de un count-min sketch crece con el flujo total (no con
la frecuencia que consultas) y el de HyperLogLog baja como 1/√m. Página de Algoritmos de streaming
(fase 10)."""

import math

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

MASCARA = (1 << 64) - 1


def mezcla(x):
    """Hash entero determinista (estilo splitmix64): misma entrada, misma salida, siempre, que es
    lo que exige una estructura de streaming cuando hay que reejecutar una tarea."""
    x = (x + 0x9E3779B97F4A7C15) & MASCARA
    x = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & MASCARA
    x = ((x ^ (x >> 27)) * 0x94D049BB133111EB) & MASCARA
    return x ^ (x >> 31)


# --- Izquierda: un flujo con una clave pesada y muchísimas claves raras. El count-min sketch no
# guarda las claves, así que las colisiones de las raras se le suman a la pesada.
FLUJO = 50_000
PESADA = 7
COLUMNAS_GRANDE, COLUMNAS_PEQUENA = 4096, 256
claves = np.where(azar.random(FLUJO) < 0.30, PESADA,
                  azar.integers(100, 100_000, FLUJO))


def indice_fila(clave, fila, columnas):
    """Columna que le toca a una clave en una fila concreta."""
    return mezcla(int(clave) * 31 + fila * 1_000_003) % columnas


def estimacion(tabla, clave):
    """La estimación es el MÍNIMO de las filas: como las colisiones solo pueden sumar, el mínimo
    es la cota más ajustada de la frecuencia real."""
    filas, columnas = tabla.shape
    return min(tabla[fila, indice_fila(clave, fila, columnas)] for fila in range(filas))


# Recorremos el flujo una sola vez llevando las dos tablas y la cuenta exacta, para ver cómo se
# separan las estimaciones del valor real a medida que el flujo crece.
pasos = np.arange(200, FLUJO + 1, 200)
FILAS = 5
tabla_g = np.zeros((FILAS, COLUMNAS_GRANDE), dtype=np.int64)
tabla_p = np.zeros((FILAS, COLUMNAS_PEQUENA), dtype=np.int64)
exacto, est_grande, est_pequena = [], [], []
cuenta = 0
for paso, clave in enumerate(claves, start=1):
    for fila in range(FILAS):
        tabla_g[fila, indice_fila(clave, fila, COLUMNAS_GRANDE)] += 1
        tabla_p[fila, indice_fila(clave, fila, COLUMNAS_PEQUENA)] += 1
    if int(clave) == PESADA:
        cuenta += 1
    if paso % 200 == 0:
        exacto.append(cuenta)
        est_grande.append(estimacion(tabla_g, PESADA))
        est_pequena.append(estimacion(tabla_p, PESADA))
exacto = np.array(exacto)
est_grande = np.array(est_grande)
est_pequena = np.array(est_pequena)
epsilon_grande = 2.718 / COLUMNAS_GRANDE      # w = e/ε, así que ε = e/w
epsilon_pequena = 2.718 / COLUMNAS_PEQUENA
cota_grande = epsilon_grande * pasos
cota_pequena = epsilon_pequena * pasos

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

ejes[0].plot(pasos, exacto, color=TEXTO, linewidth=2.0, label="recuento exacto de la clave pesada")
ejes[0].plot(pasos, est_grande, color=VERDE, linewidth=1.8,
             label=f"count-min con {COLUMNAS_GRANDE} columnas")
ejes[0].plot(pasos, est_pequena, color=AZUL, linewidth=1.8,
             label=f"count-min con {COLUMNAS_PEQUENA} columnas")
# La cota teórica ε·N: crece con el flujo total aunque la clave que consultas no crezca.
ejes[0].plot(pasos, exacto + cota_pequena, color=REJILLA, linewidth=1.6, linestyle="--",
             label=f"cota del pequeño: exacto + ε·N (ε = {epsilon_pequena:.3f})")
error_pequena = float(est_pequena[-1] - exacto[-1])
error_grande = float(est_grande[-1] - exacto[-1])
anotar(ejes[0], "el sketch nunca queda por debajo:\nsolo puede sumar de más",
       xy=(float(pasos[60]), float(est_pequena[60])), xytext=(0.04, 0.72), color=AZUL)
anotar(ejes[0], f"con pocas columnas, al final sobresestima\nen {error_pequena:.0f} ({error_pequena / exacto[-1]:.0%});\ncon muchas, solo {error_grande:.0f}",
       xy=(float(pasos[-1]), float(est_pequena[-1])), xytext=(0.30, 0.93), color=VERDE)
titulo(ejes[0], "El error del count-min no deja de crecer",
       "sobreestimación de una clave pesada a lo largo del flujo")
ejes[0].set_xlabel("elementos procesados")
ejes[0].set_ylabel("frecuencia de la clave pesada")
# La leyenda va abajo a la derecha: arriba está la separación entre la estimación y el valor real,
# que es justo lo que hay que mirar.
ejes[0].legend(loc="lower right", fontsize=7.5)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: HyperLogLog de verdad. Los b bits bajos eligen registro y del resto se cuenta el
# número de ceros iniciales; de ahí sale ρ, que estima log2 del tamaño. Cada repetición usa un
# conjunto de elementos distinto: repetir el mismo conjunto no daría error independiente, porque
# los hashes serían idénticos.
DISTINTOS = 100_000


def hyperloglog(bits, elementos):
    m = 1 << bits
    registros = np.zeros(m, dtype=np.int64)
    for valor in elementos:
        valor = int(valor)
        indice = valor & (m - 1)
        resto = valor >> bits
        # Número de ceros iniciales del resto (más uno), la magnitud que estima la cardinalidad.
        rho = 64 - bits - resto.bit_length() + 1 if resto else 64 - bits + 1
        registros[indice] = max(registros[indice], rho)
    # Corrección de sesgo para cardinalidades pequeñas: con pocos elementos muchos registros
    # siguen a cero y la fórmula cruda se dispara, así que se cuenta linealmente.
    vacios = int((registros == 0).sum())
    crudo = 0.7213 / (1 + 1.079 / m) * m * m / float(np.sum(2.0 ** (-registros)))
    if crudo <= 2.5 * m and vacios:
        return m * math.log(m / vacios)
    return crudo


bits = np.arange(4, 17)
registros_m = (2.0 ** bits).astype(int)
error_teorico = 1.04 / np.sqrt(registros_m)
error_medido = []
for b in bits:
    errores = []
    for _ in range(5):
        # Enteros de 64 bits uniformes: si los bits bajos no fueran uniformes, los registros no se
        # repartirían por igual y la estimación se dispararía.
        conjunto = azar.integers(0, 2 ** 64, DISTINTOS, dtype=np.uint64)
        estimacion_i = hyperloglog(int(b), conjunto)
        errores.append(abs(estimacion_i - DISTINTOS) / DISTINTOS)
    error_medido.append(np.median(errores))
error_medido = np.array(error_medido)

ejes[1].loglog(registros_m, error_teorico, color=AZUL, linewidth=2.0,
               label="teoría: 1,04 / √m")
ejes[1].loglog(registros_m, error_medido, color=ROJO, linewidth=1.6, linestyle=":", marker="s",
               markersize=4, label="medido, mediana de 5 tandas")
# Sin leyenda: una línea continua y unos puntos punteados se distinguen solos, y así la esquina
# de abajo queda libre para la anotación. El fondo blanco de la etiqueta la separa de la curva
# medida, que le pasa justo por debajo.
anotar(ejes[1], f"con {registros_m[-1]:,} registros (poco más de 8 kB)\n"
                f"el error medido es {error_medido[-1]:.1%}".replace(",", "."),
       xy=(float(registros_m[-1]), float(error_medido[-1])), xytext=(0.97, 0.075), color=ROJO,
       align="right", fondo=True)
titulo(ejes[1], "HyperLogLog: el error baja como 1/√m",
       "cuatro veces más registros bajan el error a la mitad")
ejes[1].set_xlabel("registros m (escala logarítmica)")
ejes[1].set_ylabel("error relativo de la cardinalidad")
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="x")

guardar(fig, "algoritmos-de-streaming-countmin-y-hll")
