"""arreglos-de-cache-y-lineas-de-cache-1.py — arriba, la escalera de la jerarquía de memoria
(tamaño contra latencia, las dos en escala logarítmica); abajo, el modelo de localidad: cuando el
conjunto de trabajo pasa del tamaño de un nivel, la tasa de fallos se dispara. Página de Arreglos
de caché y líneas de caché (fase 10)."""

import numpy as np

from comun import *

estilo()

# Cada nivel es unos 8-10 veces más grande y 3-4 veces más lento que el anterior. El último
# salto, de memoria a disco, no es un factor: es un cambio de escala.
niveles = ["Registro", "Caché L1", "Caché L2", "Caché L3", "Memoria RAM", "SSD"]
tamanos = np.array([0.00006, 32.0, 1024.0, 32768.0, 32 * 1024 * 1024.0, 512 * 1024 * 1024.0])
latencias = np.array([0.3, 1.0, 4.0, 15.0, 80.0, 100_000.0])

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

# --- Izquierda: la escalera. Una barra = un nivel, con su latencia típica.
colores = [MORADO, AZUL, CIAN, VERDE, NARANJA, ROJO]
x = np.arange(len(niveles))
ejes[0].bar(x, latencias, color=colores, width=0.62, zorder=3)
ejes[0].set_yscale("log")
ejes[0].set_xticks(x)
ejes[0].set_xticklabels(niveles, fontsize=8.5)
for xi, (tam, lat) in enumerate(zip(tamanos, latencias)):
    if tam >= 1024 * 1024:
        etiqueta = f"{tam / (1024 * 1024):.0f} MB"
    elif tam >= 1024:
        etiqueta = f"{tam / 1024:.0f} MB"
    elif tam >= 1:
        etiqueta = f"{tam:.0f} KB"
    else:
        etiqueta = "64 B"
    texto = f"{lat:g} ns" if lat < 1000 else f"{lat / 1000:g} us"
    # El tamaño va SOBRE la barra, no dentro: una barra de 0,3 ns mide dos píxeles y el texto
    # se salía por los lados.
    ejes[0].text(xi, lat * 1.35, f"{texto}\n{etiqueta}", ha="center", va="bottom", fontsize=8,
                 color=TEXTO, linespacing=1.3)
anotar(ejes[0], "de RAM a SSD la espera se mide\nen decenas de microsegundos: 1000 veces más",
       xy=(5, 100_000.0), xytext=(0.22, 0.84), color=ROJO)
anotar(ejes[0], "la caché no es magia: son unos pocos\nmegabytes que caben al lado del núcleo",
       xy=(2, 4.0), xytext=(0.03, 0.44), color=CIAN)
titulo(ejes[0], "Cada nivel es mayor y más lento",
       "latencia típica de acceso y tamaño; las dos escalas son logarítmicas")
ejes[0].set_ylabel("latencia del acceso (nanosegundos)")
rejilla(ejes[0], eje="y")

# --- Derecha: el modelo de localidad. Cada nivel se lleva su parte de los fallos que deja el
# anterior, y ese reparto no es gradual: es un codo.
RAM = 64 * 1024 * 1024.0
umbrales = [32.0, 1024.0, 32768.0, RAM]
colores_nivel = [AZUL, CIAN, VERDE, NARANJA, ROJO]
trabajo = np.logspace(2, np.log10(RAM), 400)
restante = np.ones_like(trabajo)
procedencia = []
for umbral in umbrales:
    # Dos tramos: hasta que el conjunto de trabajo cabe (fallo residual) y a partir de ahí, caída
    # en ley de potencias. El exponente se eligió para que el codo se vea como tal.
    frac = np.where(trabajo <= umbral, 0.02, 0.55 * (trabajo / umbral) ** (-0.45))
    procedencia.append(restante * frac)
    restante = restante * (1 - frac)
procedencia.append(restante)
etiquetas = ["L1 (32 KB)", "L2 (1 MB)", "L3 (32 MB)", "RAM (64 MB)", "fallo de página"]
ejes[1].stackplot(trabajo / 1024, *[p * 100 for p in procedencia], colors=colores_nivel, alpha=0.85)
ejes[1].set_xscale("log")
for umbral, color in zip(umbrales, colores_nivel[:-1]):
    posicion = umbral / 1024
    ejes[1].axvline(posicion, color=TEXTO, linewidth=0.9, linestyle=":")
    if umbral <= 32:
        etiqueta_codo = "L1: 32 KB"
    elif umbral <= 1024:
        etiqueta_codo = "L2: 1 MB"
    elif umbral <= 32768:
        etiqueta_codo = "L3: 32 MB"
    else:
        etiqueta_codo = "RAM"
    if umbral == umbrales[-1]:
        # El último umbral cae en el borde derecho: la etiqueta va hacia dentro, pegada a la línea.
        altura = 78.0
        ejes[1].text(posicion * 0.93, altura, etiqueta_codo, fontsize=7, color=TEXTO, rotation=90,
                     va="top", ha="left", bbox=dict(facecolor="white", edgecolor="none", pad=0.8))
    else:
        # Rotado y pegado a su línea, pero a alturas distintas: cuatro etiquetas verticales al
        # mismo nivel se pisaban entre ellas (32 KB y 1 MB caen a un 1,5 % de distancia en log).
        altura = 86 - 15 * float(np.log10(posicion / 0.03125))
        ejes[1].text(posicion * 1.03, altura, etiqueta_codo, fontsize=7, color=TEXTO, rotation=90,
                     va="top", ha="left", bbox=dict(facecolor="white", edgecolor="none", pad=0.8))
anotar(ejes[1], "mientras el conjunto de trabajo cabe,\nlos fallos no cambian de nivel",
       xy=(8.0, 88.0), xytext=(0.40, 0.72), color=AZUL, fondo=True)
anotar(ejes[1], "al desbordar un nivel, la carga se muda\nentera al siguiente",
       xy=(60000.0, 55.0), xytext=(0.05, 0.42), color=NARANJA, fondo=True)
titulo(ejes[1], "El codo está en el tamaño del nivel",
       "reparto de los accesos: el área de cada color es la fracción que atiende ese nivel")
ejes[1].set_xlabel("conjunto de trabajo (kilobytes, escala logarítmica)")
ejes[1].set_ylabel("porcentaje de los accesos")
ejes[1].set_ylim(0, 100)
leyenda = ejes[1].legend(etiquetas, loc="lower left", fontsize=7.0, ncol=2, frameon=True)
leyenda.get_frame().set_facecolor("white")
leyenda.get_frame().set_edgecolor("none")
numeros(ejes[1], ejes="x")

guardar(fig, "cache-escalera-y-codo-de-localidad")
