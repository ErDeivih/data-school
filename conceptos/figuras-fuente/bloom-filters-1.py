"""bloom-filters-1.py — la tasa de falsos positivos no depende solo de la memoria: depende de
cuántos elementos has insertado (m/n) y de cuántas funciones hash uses. Página de Filtros de Bloom
(fase 10)."""

import hashlib

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)


def posiciones(elemento, k, m):
    """Doble hashing: dos hashes independientes y el resto se generan combinándolos. Es lo que se
    hace en la práctica, porque calcular k hashes distintos es k veces más caro."""
    h1 = int.from_bytes(hashlib.blake2b(elemento, digest_size=8, person=b"b1").digest(), "big")
    h2 = int.from_bytes(hashlib.blake2b(elemento, digest_size=8, person=b"b2").digest(), "big")
    return [((h1 + i * h2) % m) for i in range(k)]


def falso_positivo_medido(m, k, n, ausentes):
    """Construye el filtro de verdad: inserta n elementos y cuenta cuántos de los ausentes pasan
    el filtro. Devuelve la tasa medida, no la teórica."""
    bits = np.zeros(m, dtype=bool)
    for i in range(n):
        bits[posiciones(b"presente" + str(i).encode(), k, m)] = True
    aciertos = sum(all(bits[posiciones(b"ausente" + str(i).encode(), k, m)]) for i in range(ausentes))
    return aciertos / ausentes


fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

# --- Izquierda: con la memoria fija (1 MB = 8 millones de bits), el error crece al llenar.
BITS = 8_000_000
elementos = np.linspace(100_000, 4_000_000, 200)
K_DISENO = 5


def tasa(k, n, m=BITS):
    """p ≈ (1 − e^(−k·n/m))^k, la probabilidad de que los k bits consultados estén todos a 1."""
    return (1 - np.exp(-k * n / m)) ** k


# Con k calculado para el n de diseño (1 millón, 8 bits por elemento): k = 8·ln2 ≈ 5,5 → 5 o 6.
diseno = 1_000_000
k_optimo = (BITS / diseno) * np.log(2)
# Y la variante que reajusta k para cada tamaño, que es lo que haría un filtro bien dimensionado.
k_variable = np.maximum(1, np.round((BITS / elementos) * np.log(2)))

ejes[0].semilogy(elementos / 1e6, tasa(K_DISENO, elementos), color=AZUL, linewidth=2.0,
                 label=f"k = {K_DISENO} fijo")
ejes[0].semilogy(elementos / 1e6, tasa(k_variable, elementos), color=NARANJA, linewidth=2.0,
                 linestyle="--", label="k recalculado para cada n")
ejes[0].plot(diseno / 1e6, tasa(K_DISENO, diseno), marker="o", markersize=9, color=ROJO, zorder=5)
ejes[0].axvline(diseno / 1e6, color=REJILLA, linewidth=1.1, linestyle=":")
p_diseno = float(tasa(K_DISENO, diseno))
p_doble = float(tasa(K_DISENO, 2 * diseno))
# Las dos curvas van rotuladas sobre sí mismas en vez de con leyenda: así la esquina de abajo a la
# derecha queda libre para la nota larga.
anotar(ejes[0], f"k = {K_DISENO} fijo", xy=(1.4, float(tasa(K_DISENO, 1_400_000))),
       xytext=(0.58, 0.50), color=AZUL)
anotar(ejes[0], "k recalculado para cada n", xy=(1.0, float(tasa(6, 1_000_000))),
       xytext=(0.58, 0.38), color=NARANJA)
anotar(ejes[0], f"el punto de diseño: 8 bits por elemento\ny k = {K_DISENO} dan un {p_diseno:.1%}",
       xy=(diseno / 1e6, p_diseno), xytext=(0.97, 0.09), color=ROJO, align="right")
anotar(ejes[0], f"si insertas el doble de lo previsto\nel error sube al {p_doble:.1%}, "
                f"{p_doble / p_diseno:.0f} veces más",
       xy=(2.0, p_doble), xytext=(0.30, 0.88), color=AZUL, fondo=True)
titulo(ejes[0], "Sin crecer, el filtro se degrada al llenarse",
       "1 MB de bits (8 millones) y una tasa de error objetivo del 2 %")
ejes[0].set_xlabel("elementos insertados (millones)")
ejes[0].set_ylabel("tasa de falsos positivos (escala logarítmica)")
# El eje se corta en 1e-5: por debajo la curva ya es plana y no enseña nada, y así se ve con
# detalle el tramo que importa.
ejes[0].set_ylim(1e-5, 1.5)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="x")

# --- Derecha: la curva en U del número de funciones hash. Con m/n = 8 bits por elemento, el
# óptimo teórico es k = 8·ln2 ≈ 5,5, y alrededor de él la curva es muy plana.
M_PRUEBA, N_PRUEBA = 800_000, 100_000
valores_k = np.arange(1, 17)
teorico = np.array([float(tasa(k, N_PRUEBA, M_PRUEBA)) for k in valores_k])
medido = np.array([falso_positivo_medido(M_PRUEBA, int(k), N_PRUEBA, 20_000) for k in valores_k])
mejor = int(valores_k[np.argmin(teorico)])

ejes[1].semilogy(valores_k, teorico, color=AZUL, linewidth=2.0, marker="o", markersize=4,
                 label="teoría: (1 − e^(−k·n/m))^k")
ejes[1].semilogy(valores_k, medido, color=ROJO, linewidth=1.5, linestyle=":", marker="s",
                 markersize=4, label="medido con el filtro de verdad")
anotar(ejes[1], f"el mínimo está en k = {mejor} y la curva\nes plana alrededor: de 5 a 7 no cambia",
       xy=(float(mejor), float(teorico[mejor - 1])), xytext=(0.30, 0.70), color=AZUL)
anotar(ejes[1], "con k = 1 el filtro se satura enseguida;\ncon k = 16 se llena casi todo",
       xy=(16.0, float(teorico[-1])), xytext=(0.30, 0.88), color=ROJO)
titulo(ejes[1], "Hay un número óptimo de funciones hash",
       "8 bits por elemento: la teoría manda y la medición la sigue")
ejes[1].set_xlabel("k: número de funciones hash")
ejes[1].set_ylabel("tasa de falsos positivos (escala logarítmica)")
ejes[1].set_xticks(valores_k[::2])
ejes[1].legend(loc="upper left", fontsize=8)
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="both")

guardar(fig, "bloom-filters-k-y-llenado")
