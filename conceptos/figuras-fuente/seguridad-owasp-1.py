"""seguridad-owasp-1.py — que devuelve la misma entrada hostil segun como se construya la
consulta: concatenando el texto crecen las filas que salen en la respuesta, y con parámetro
la respuesta no depende del texto. La figura de la pagina de seguridad de aplicaciones (fase 11)."""

import numpy as np

from comun import *

estilo()

# Usuarios que hay en la tabla: cuanto mas grande es la tabla, mas se nota el fallo.
usuarios = np.arange(1, 11)
concatenando = usuarios.astype(float)   # la condicion queda siempre verdadera: salen todas
correo_real = np.ones(usuarios.size)    # con parametro y un correo que existe: una sola
parametro = np.zeros(usuarios.size)     # con parametro, el texto hostil no coincide con nadie

fig, ax = plt.subplots(figsize=(7.6, 4.2))

ax.plot(usuarios, concatenando, color=ROJO, linewidth=1.8, marker="o", markersize=4.5,
        label="concatenando el texto del usuario")
ax.plot(usuarios, correo_real, color=AZUL, linewidth=1.8, marker="s", markersize=4.5,
        label="con parámetro y un correo que existe")
ax.plot(usuarios, parametro, color=VERDE, linewidth=1.8, marker="^", markersize=4.5,
        label="con parámetro y la entrada hostil")

# La anotacion va arriba a la izquierda, el unico hueco que deja la diagonal.
anotar(ax, "con un solo usuario, concatenar también\ndevuelve una fila: el fallo no se ve",
       xy=(1, 1), xytext=(0.05, 0.66), color=ROJO)
anotar(ax, "con diez usuarios salen las diez filas",
       xy=(10, 10), xytext=(0.52, 0.94), color=ROJO)

ax.set_xlabel("usuarios en la tabla")
ax.set_ylabel("filas devueltas")
ax.set_ylim(-0.7, 12.4)
ax.set_xlim(0.4, 10.6)
titulo(ax, "La misma entrada hostil, tres resultados",
       "parametrizar hace que el resultado no dependa del texto")
rejilla(ax)
numeros(ax)
ax.legend(loc="upper center", ncols=1, bbox_to_anchor=(0.5, -0.20))

guardar(fig, "seguridad-owasp-filas-devuelta")
