"""cnn-1.py — qué mira un filtro, dónde responde y por qué moverse no lo despista.

Arriba: una barra vertical sobre fondo vacío y la respuesta de un filtro de borde vertical,
que da un pico a cada lado. Abajo: la misma barra desplazada cuatro píxeles y su respuesta,
que se desplaza igual con los mismos 27 pesos. Eso es la equivarianza a la traslación, y es
la razón de que una convolución reconozca el patrón esté donde esté.
La figura de la página de redes convolucionales (fase 7).
"""

import numpy as np

from comun import *

estilo()

LADO = 16                                  # imagen cuadrada de 16x16 píxeles
FILA0, FILA1 = 4, 12                       # la barra no llega arriba: deja sitio a la nota


def barra(columna):
    """Imagen de fondo cero con una barra vertical de dos píxeles de ancho."""
    img = np.zeros((LADO, LADO))
    img[FILA0:FILA1, columna:columna + 2] = 1.0
    return img


def correlacion(img, filtro):
    """Correlación cruzada 2D con relleno de ceros: la salida mide igual que la entrada.

    Es lo que hace una capa convolucional (sin girar el filtro): en cada posición se
    multiplica la ventana por los pesos del filtro y se suma.
    """
    f = filtro.shape[0]
    borde = f // 2                                  # relleno que conserva el tamaño
    relleno = np.pad(img, borde)                    # np.pad añade ceros alrededor
    salida = np.zeros_like(img, dtype=float)
    for i in range(LADO):
        for j in range(LADO):
            salida[i, j] = (relleno[i:i + f, j:j + f] * filtro).sum()
    return salida


def pinta(ax, valores, color):
    """Dibuja una magnitud con un solo color: opaco donde es grande, transparente en cero.

    Se usa alpha en vez de una escala de color completa para quedarse dentro de la paleta
    del modulo: el cero desaparece y solo se ve lo que el filtro detecta.
    """
    escala = matplotlib.colors.LinearSegmentedColormap.from_list("tono", [color, color])
    tope = float(np.abs(valores).max()) or 1.0
    ax.imshow(valores, cmap=escala, vmin=0.0, vmax=1.0,
              alpha=np.clip(np.abs(valores) / tope, 0.0, 1.0))


# Filtro de borde vertical: negativo a la izquierda, positivo a la derecha.
FILTRO = np.array([[-1.0, 0.0, 1.0]] * 3)

fig, ejes = plt.subplots(2, 2, figsize=(8.6, 7.6))

for fila, col in enumerate((5, 9)):
    img = barra(col)
    resp = correlacion(img, FILTRO)
    col_pico = int(np.argmax(np.abs(resp).sum(axis=0)))   # columna que más responde

    ax = ejes[fila, 0]
    pinta(ax, img, AZUL)
    # La ventana 3x3 del filtro: el mismo rectangulo que se desliza por toda la imagen.
    ax.add_patch(matplotlib.patches.Rectangle((col - 1.5, 5.5), 3, 3, fill=False,
                                              edgecolor=TEXTO, linewidth=1.3,
                                              linestyle="--"))
    if fila == 0:
        anotar(ax, "el filtro lee esta ventana", xy=(col + 0.5, 5.5), xytext=(0.04, 0.86))
    ax.set_xlabel("columna de píxel")
    ax.set_ylabel("fila de píxel")
    titulo(ax, "La barra y la ventana del filtro" if fila == 0
           else "La misma barra, 4 píxeles a la derecha",
           "16x16 píxeles: cero en el fondo y una barra de dos columnas" if fila == 0
           else "el filtro es el mismo: no hay pesos distintos por posición")

    ax = ejes[fila, 1]
    pinta(ax, np.clip(resp, 0.0, None), AZUL)      # subidas: azul
    pinta(ax, np.clip(-resp, 0.0, None), ROJO)     # bajadas: rojo
    if fila == 0:
        anotar(ax, "un pico a cada lado del borde", xy=(col_pico, 8.0),
               xytext=(0.04, 0.88), color=AZUL)
    else:
        anotar(ax, "el pico se ha movido igual", xy=(col_pico, 11.0),
               xytext=(0.04, 0.10), color=VERDE)
    ax.set_xlabel("columna de píxel")
    titulo(ax, "Dónde responde el filtro" if fila == 0
           else "La respuesta se desplaza igual",
           "azul: de cero a uno.  rojo: de uno a cero" if fila == 0
           else "equivarianza a la traslación: nada más cambia")

    for a in (ejes[fila, 0], ejes[fila, 1]):
        # En una imagen de píxeles la rejilla solo añade ruido: se quitan las marcas.
        numeros(a)
        rejilla(a)
        a.set_xticks([])
        a.set_yticks([])

guardar(fig, "cnn-ventana-y-respuesta")
