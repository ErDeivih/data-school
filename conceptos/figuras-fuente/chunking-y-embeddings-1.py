"""chunking-y-embeddings-1.py — el tamaño del trozo y el solapamiento deciden lo que se
encuentra. Las dos mitades del compromiso: sin solape la frase clave se parte en dos, y una
ventana muy grande promedia varios asuntos y diluye la similitud. Figura de la pagina de
troceado y embeddings (fase 8)."""

import numpy as np

from comun import *

estilo()

# Mismo documento de juguete que la pagina: 137 caracteres, dos frases utiles.
DOC = ("La factura se emite el dia 1. El plazo de pago es de 30 dias "
       "desde la fecha de emisión. Los pagos tardios devengan un interes del 3,75 %.")
CONSULTA = "interes por pagos tardios"


def trozos(texto, w, s):
    return [texto[i:i + w] for i in range(0, len(texto), s)]


def dispersion(texto, dim=256):
    """Indice de la posición que ocupa una palabra: hash determinista (el mismo en cada
    ejecución, a diferencia del hash() de Python, que cambia de proceso a proceso)."""
    valor = 0
    for letra in texto:
        valor = (valor * 31 + ord(letra)) % dim
    return valor


def embedding(texto, dim=256):
    """Bolsa de palabras + bigramas con hashing trick, igual que el bloque de la pagina."""
    palabras = texto.lower().split()
    piezas = list(palabras) + [a + "_" + b for a, b in zip(palabras, palabras[1:])]
    v = np.zeros(dim)
    for p in piezas:
        v[dispersion(p, dim)] += 1.0
    return v


def similitud(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(a @ b / (na * nb)) if na and nb else 0.0


# --- Panel izquierdo: que trozos conservan entera la frase clave -------------------
salto = (34, 24)
integridad = [sum("pagos tardios" in t for t in trozos(DOC, 34, s)) for s in salto]

# --- Panel derecho: la similitud segun crece la ventana ---------------------------
ventanas = [12, 15, 18, 22, 26, 30, 34, 40, 48, 58, 70]


def mejor_similitud(w):
    """La similitud más alta que consigue cualquier trozo de tamaño w (el top-1)."""
    return max(similitud(embedding(t), embedding(CONSULTA)) for t in trozos(DOC, w, 34))


mejores = np.array([mejor_similitud(w) for w in ventanas])
i_mejor = int(np.argmax(mejores))
w_mejor = ventanas[i_mejor]

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.1))

# Panel 1: cuantos fragmentos contienen la frase entera
colores = [ROJO, VERDE]
posiciones = [0, 1]
barras = ejes[0].bar(posiciones, integridad, color=colores, width=0.5)
ejes[0].set_xlim(-0.6, 1.6)
for barra, valor in zip(barras, integridad):
    # La barra nula no tiene altura: su etiqueta sube algo mas para no caer sobre el eje.
    ejes[0].annotate("ninguno" if valor == 0 else f"{valor} de {len(trozos(DOC, 34, 24))}",
                     (barra.get_x() + barra.get_width() / 2, valor),
                     textcoords="offset points", xytext=(0, 14 if valor == 0 else 5),
                     ha="center", color=TEXTO, fontsize=10)
ejes[0].set_ylim(0, 1.5)
ejes[0].set_yticks([0, 1])
titulo(ejes[0], "Sin solapar, la frase clave se parte",
       "con solape, un trozo la contiene entera")
ejes[0].set_ylabel("fragmentos con la frase completa")
rejilla(ejes[0])
numeros(ejes[0])
# Los nombres de las categorias van DESPUES de numeros(): su formateador reescribe las
# etiquetas del eje x y borraria las que se hubieran puesto antes.
ejes[0].set_xticks(posiciones)
ejes[0].set_xticklabels(["sin solape (salto 34)", "con solape (salto 24)"])

# Panel 2: la similitud frente al tamano de la ventana
ejes[1].plot(ventanas, mejores, color=AZUL, linewidth=1.8)
ejes[1].plot([w_mejor], [mejores[i_mejor]], "o", color=AZUL, markersize=5)
# Cada nota va a un hueco distinto: el maximo arriba, la ventana corta debajo del salto y el
# trozo grande en el hueco de abajo a la derecha, que si no se sale por el borde.
anotar(ejes[1], f"máximo con {w_mejor} caracteres",
       xy=(w_mejor, mejores[i_mejor]), xytext=(0.30, 0.82), color=AZUL)
for w in (15, 34, 70):
    indice = ventanas.index(w)
    ejes[1].plot([w], [mejores[indice]], "o", color=ROJO, markersize=5)
anotar(ejes[1], "la ventana se queda\nsin la palabra que responde",
       xy=(15, 0.0), xytext=(0.20, 0.10), color=ROJO)
anotar(ejes[1], "la misma frase, diluida\nentre más texto",
       xy=(70, mejores[ventanas.index(70)]), xytext=(0.62, 0.42), color=ROJO)
titulo(ejes[1], "La similitud sube y luego baja", "el trozo grande diluye la pregunta")
ejes[1].set_xlabel("tamaño del fragmento (caracteres)")
ejes[1].set_ylabel("mejor similitud con la consulta")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "chunking-frontera-y-tamano")
