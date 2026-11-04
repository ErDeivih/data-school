from collections import defaultdict

documentos = {
    "d1": "el gato come pescado",
    "d2": "el perro come pienso",
    "d3": "el gato y el perro duermen",
}


def map_(texto):
    for palabra in texto.split():
        yield palabra, 1          # cada palabra cuenta uno en su propio documento


def reduce_(clave, valores):
    return clave, sum(valores)    # el reductor solo ve los valores de su clave


pares = [par for texto in documentos.values() for par in map_(texto)]
grupos = defaultdict(list)
for clave, valor in pares:
    grupos[clave].append(valor)   # el shuffle manda cada clave a un unico reductor

recuento = dict(reduce_(*grupo) for grupo in grupos.items())
print("pares emitidos por el map:", len(pares))   # -> 14
print("palabras distintas:", len(recuento))       # -> 8
print("el:", recuento["el"], "gato:", recuento["gato"], "come:", recuento["come"])
# la ultima linea imprime: el: 4 gato: 2 come: 2
