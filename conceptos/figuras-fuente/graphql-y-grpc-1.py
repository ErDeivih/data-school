"""graphql-y-grpc-1.py — las dos facturas que se pagan al elegir estilo: las consultas que
genera el N+1 y los bytes que solo son estructura. La figura de la página de GraphQL y gRPC
(fase 11).

Los dos títulos de dos líneas se comían la mitad de cada panel. Van cortos, con la cuenta en
el subtítulo, y la nota de la izquierda se coloca debajo de la barra alta en vez de al lado
(antes se cruzaba con su etiqueta y con la barra). A la derecha se ensancha el eje para que la
etiqueta de 44 bytes no salga por el borde."""

import json

import numpy as np

from comun import *

estilo()

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.0))

# --- Izquierda: consultas a la base de datos para pintar 100 pedidos ------------------
estilos = ["REST\n(el endpoint trae\nel cliente)", "GraphQL\ncon batching", "GraphQL\nsin batching\n(N+1)"]
consultas = np.array([1, 2, 101])
barras = izq.bar(estilos, consultas, color=[AZUL, VERDE, ROJO], width=0.6)
izq.bar_label(barras, padding=3, fontsize=9)
izq.set_ylim(0, 120)
# La nota va debajo de la barra alta: la flecha que la unía a la etiqueta cruzaba los ticks.
izq.annotate("1 consulta para la lista\ny 100 para los clientes",
             xy=(2, 70), xytext=(0.52, 0.42), textcoords="axes fraction",
             ha="center", va="top", color=ROJO, fontsize=9)
titulo(izq, "La misma pantalla: 101 consultas o 2",
       "según quién resuelva los clientes de la lista")
izq.set_ylabel("consultas a la base de datos")
rejilla(izq)
numeros(izq, ejes="y")

# --- Derecha: de qué están hechos los bytes de una respuesta --------------------------
datos = {"id": 42, "total": 412.5, "cliente": "Ana"}
# Los tres valores son los mismos en los dos formatos y pesan lo mismo: 2 + 5 + 5 caracteres.
valores = 2 + 5 + 5
# JSON: el resto del texto son los nombres de campo, las llaves, los dos puntos y las comas.
estructura_json = len(json.dumps(datos)) - valores
# protobuf: un tag de 1 byte por campo más el byte de longitud de "Ana"; el entero y el double
# van sin nombre y sin separadores (1 byte de varint y 8 bytes fijos).
estructura_protobuf = 3 + 1
valores_protobuf = 1 + 8 + 3

medidas = [("JSON (REST)", estructura_json, valores, ROJO),
           ("protobuf (gRPC)", estructura_protobuf, valores_protobuf, REJILLA)]
for y, (etiqueta, estructura, carga, color) in enumerate(medidas):
    der.barh(y, estructura, color=color, height=0.5,
             label="estructura: nombres de campo, tags, llaves y comas" if y == 0 else None)
    der.barh(y, carga, left=estructura, color=AZUL, height=0.5,
             label="valores" if y == 0 else None)
    total = estructura + carga
    der.text(total + 1.2, y, f"{total} bytes · {estructura} de estructura", va="center", fontsize=9)
der.set_yticks([0, 1], [m[0] for m in medidas])
der.set_ylim(-0.75, 1.8)
der.invert_yaxis()                     # JSON arriba: es el punto de partida de la comparación
# El eje llega hasta 100 y no hasta 76: la etiqueta de la barra mas larga ("44 bytes...") no
# cabia dentro y se salia del lienzo.
der.set_xlim(0, 100)
der.set_xlabel("bytes del mismo mensaje")
titulo(der, "Mismos valores, distinta estructura",
       "los valores son 12 bytes en los dos: la estructura es 32 frente a 4")
der.legend(loc="lower right")
rejilla(der, eje="x")
numeros(der, ejes="x")

guardar(fig, "graphql-y-grpc-consultas-y-bytes")
