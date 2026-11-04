"""evolucion-de-esquema-1.py — que cambios de esquema puede leer cada versión del lector.
La matriz responde a la pregunta que de verdad importa antes de tocar nada: si público
este cambio, quien sigue leyendo con el codigo viejo y con el nuevo. La segunda parte
ensena que el formato columnar no borra lo ya escrito: cada fichero conserva las columnas
que tenia, y quien lee varios ficheros juntos rellena con nulo lo que falta.
"""

import numpy as np

from comun import *

estilo()

fig, (izq, der) = plt.subplots(1, 2, figsize=(10.6, 4.0), gridspec_kw={"width_ratios": [1.85, 1]})

# --- Panel izquierdo: matriz cambio x version del lector --------------------------
cambios = [
    "anadir columna\ncon valor por defecto",
    "anadir columna\nopcional (nulo)",
    "hacer opcional\nuna obligatoria",
    "renombrar\nuna columna",
    "cambiar el tipo\n(entero a texto)",
    "reordenar\ncolumnas",
    "quitar\nuna columna",
]
lectores = ["lector v1\n(codigo viejo)", "lector v2\n(lee por nombre)", "lector v3\n(lee por posición)"]
# 2 = compatible, 1 = depende de como lea, 0 = rompe.
# 2 = compatible, 1 = depende de como lea (o de donde se anada la columna), 0 = rompe.
# Las filas tienen que decir lo mismo que la tabla de compatibilidad de la pagina: al lector
# que va por posicion le rompe cualquier columna que se cuele en medio, tenga valor por
# defecto o no; y hacer opcional una obligatoria no mueve ninguna posicion.
compatible = np.array([
    [2, 2, 1],      # anadir columna con valor por defecto: si va al final si, en medio no
    [2, 2, 1],      # anadir columna opcional (nulo): igual, depende de donde se ponga
    [2, 2, 2],      # hacer opcional una obligatoria: no mueve posiciones
    [0, 1, 0],      # renombrar una columna
    [0, 1, 0],      # cambiar el tipo (entero a texto)
    [2, 2, 0],      # reordenar columnas
    [0, 0, 0],      # quitar una columna
])

mapa = np.array([TEXTO, NARANJA, VERDE])
im = izq.imshow(compatible, cmap=matplotlib.colors.ListedColormap(mapa), vmin=0, vmax=2)
izq.set_xticks(range(len(lectores)))
izq.set_xticklabels([""] * len(lectores))
izq.set_yticks(range(len(cambios)))
izq.set_yticklabels(cambios, fontsize=8.5)
izq.set_title("Cada cambio se juzga contra quien ya lee la tabla")
for f in range(len(cambios)):
    for c in range(len(lectores)):
        marca = {2: "si", 1: "?", 0: "no"}[compatible[f, c]]
        izq.text(c, f, marca, ha="center", va="center", color="white", fontsize=9, fontweight="bold")
# Los nombres de los lectores van girados: en horizontal se solaparian entre si.
for c, nombre in enumerate(["lector v1 (codigo viejo)", "lector v2 (lee por nombre)",
                            "lector v3 (lee por posición)"]):
    izq.text(c, len(cambios) - 0.42, nombre, ha="right", va="top", rotation=32,
             rotation_mode="anchor", color=TEXTO, fontsize=8.5)
izq.set_xticks(np.arange(-0.5, len(lectores), 1), minor=True)
izq.set_yticks(np.arange(-0.5, len(cambios), 1), minor=True)
izq.grid(which="minor", color="white", linewidth=1.4)
izq.tick_params(which="minor", length=0)
izq.spines["top"].set_visible(False)
izq.spines["right"].set_visible(False)

# --- Panel derecho: lo escrito no cambia aunque cambie el esquema -----------------
# Cada fichero se escribio con las columnas que entonces existian: el motor rellena
# con nulo las que faltan, y ese nulo no se puede distinguir de un dato ausente real.
escritos = ["fichero de enero", "fichero de febrero", "fichero de marzo"]
columnas = ["id", "importe", "ciudad", "canal"]
presente = np.array([
    [1, 1, 1, 0],
    [1, 1, 1, 0],
    [1, 1, 1, 1],
])
der.imshow(presente, cmap=matplotlib.colors.ListedColormap([REJILLA, AZUL]), vmin=0, vmax=1)
der.set_xticks(range(len(columnas)))
der.set_xticklabels(columnas, fontsize=9)
der.set_yticks(range(len(escritos)))
der.set_yticklabels(escritos, fontsize=9)
der.set_title("La columna nueva solo existe en lo escrito después")
for f in range(len(escritos)):
    for c in range(len(columnas)):
        texto = "dato" if presente[f, c] else "nulo"
        der.text(c, f, texto, ha="center", va="center", color="white", fontsize=8.5)
der.set_xticks(np.arange(-0.5, len(columnas), 1), minor=True)
der.set_yticks(np.arange(-0.5, len(escritos), 1), minor=True)
der.grid(which="minor", color="white", linewidth=1.4)
der.tick_params(which="minor", length=0)
der.spines["top"].set_visible(False)
der.spines["right"].set_visible(False)

guardar(fig, "evolucion-de-esquema-compatibilidad")
