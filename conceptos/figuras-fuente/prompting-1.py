"""prompting-1.py — el presupuesto de la ventana es una resta: lo que se lleva el
prompt no se lo lleva la respuesta. La figura de la pagina de prompts (fase 8)."""

import numpy as np

from comun import *

estilo()

# Dos filas: el panel de las barras necesita el ancho entero para que la etiqueta de cada
# caso quepa a la derecha de su barra, y el de la curva respira mejor estirado.
fig, (arriba, abajo) = plt.subplots(2, 1, figsize=(9.8, 8.0))

# --- Panel de arriba: tres prompts, tres margenes para la respuesta -----------
casos = [
    ("Medido con 2 caracteres\npor token: 12.700", 12700),
    ("Prompt ajustado: 3.996", 3996),
    ("Prompt del ejemplo: 6.350", 6350),
]
ventana = 4096

for i, (etiqueta, usado) in enumerate(casos):
    prompt = min(usado, ventana)
    respuesta = max(ventana - usado, 0)
    arriba.barh(i, prompt, color=AZUL)
    if respuesta:
        arriba.barh(i, respuesta, left=prompt, color=VERDE)
    else:
        # Cuando el prompt se pasa, no queda hueco: lo que sobra se recorta
        arriba.barh(i, usado - ventana, left=ventana, color=ROJO)
    margen = ventana - usado
    texto = f"quedan {margen} para la respuesta" if margen >= 0 else f"sobran {-margen}: se recorta el contexto"
    color = TEXTO if margen >= 0 else ROJO
    # El texto arranca donde acaba la barra mas larga de su fila: a la derecha de ahi no hay
    # nada dibujado, asi que no tapa ni el azul, ni el verde, ni el rojo.
    arriba.text(max(usado, ventana) + 500, i, texto, va="center", fontsize=8.5, color=color)

arriba.axvline(ventana, color=TEXTO, linewidth=1.0, linestyle="--")
# Por encima de la barra de arriba (que acaba en y = 2,4) queda libre la franja del titulo.
arriba.text(ventana + 250, 2.62, "limite de la ventana", fontsize=8.5, color=TEXTO)
arriba.set_yticks(range(3))
arriba.set_yticklabels([c[0] for c in casos], fontsize=8.5)
arriba.set_xlim(-600, 19000)
arriba.set_ylim(-0.6, 2.9)
# Cuatro marcas en vez de las ocho que salian solas: antes se solapaban entre si.
arriba.set_xticks([0, 4000, 8000, 12000, 16000])
arriba.set_xlabel("tokens")
titulo(arriba, "El prompt se come el presupuesto",
      "Azul: el prompt · Verde: hueco para responder · Rojo: lo que ya no cabe")
rejilla(arriba, "x")
numeros(arriba, "x")

# --- Panel de abajo: contar caracteres no es contar tokens ---------------------
fracciones = np.linspace(2.0, 5.0, 100)
abajo.plot(fracciones, 12700 * 2 / fracciones, color=MORADO, linewidth=1.8)
abajo.axhline(4096, color=ROJO, linewidth=1.2, linestyle="--")
abajo.fill_between(fracciones, 4096, 12700 * 2 / fracciones,
                   where=(12700 * 2 / fracciones > 4096), color=ROJO, alpha=0.12)
# La curva baja de izquierda a derecha: por encima de ella, a la derecha, no hay nada.
anotar(abajo, "la misma entrada cabe o no cabe\nsegún la regla que uses",
       xy=(3.0, 12700 * 2 / 3.0), xytext=(0.42, 0.72), color=ROJO)
# La franja de debajo de la linea de 4.096, a la izquierda, tambien esta vacia.
anotar(abajo, "ventana de 4.096 tokens", xy=(3.2, 4096), xytext=(0.06, 0.12), color=ROJO)
abajo.set_ylim(1500, 13500)
abajo.set_xlabel("caracteres por token que supones")
abajo.set_ylabel("tokens estimados")
titulo(abajo, "La regla de 4 caracteres se queda corta")
rejilla(abajo)
numeros(abajo)

guardar(fig, "prompting-presupuesto-de-la-ventana")
