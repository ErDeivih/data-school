import re
from collections import Counter

casos = [
    ("capital de Francia", "Paris", "Paris"),
    ("capital de Francia", "Paris", "paris"),
    ("capital de Francia", "Paris", "Lyon"),
    ("ano de la Revolucion Francesa", "1789", "en 1789"),
    ("ano de la Revolucion Francesa", "1789", "1799"),
    ("unidad de potencia", "vatio", "el vatio"),
]

def normalizar(t):
    # [^\w\s] es "todo lo que no sea letra ni espacio": asi "París" y "paris" se comparan
    # igual. \w incluye las vocales acentuadas, ojo: no las quita, solo quita la puntuacion.
    return re.sub(r"[^\w\s]", "", t.lower()).split()   # minusculas y sin puntuacion

def f1(pred, ref):
    p, r = Counter(normalizar(pred)), Counter(normalizar(ref))
    # p & r es la interseccion de multiconjuntos: cuenta las palabras comunes
    # el minimo de repeticiones, no una vez por aparicion en cualquiera de los dos
    comunes = sum((p & r).values())                    # interseccion multiconjunto
    if comunes == 0:
        return 0.0
    # P y R por separado: el F1 es su media armonica, no la media normal
    precision = comunes / sum(p.values())
    recall = comunes / sum(r.values())
    return 2 * precision * recall / (precision + recall)

# una sola pasada por los casos: la tupla guarda la referencia y las dos metricas
filas = [(p, g, normalizar(p) == normalizar(g), f1(p, g)) for _, p, g in casos]
for p, g, exacta, f in filas:
    # {p!r} imprime el valor con sus comillas: se ve que "paris" y "Paris" son distintos
    print(f"pred {p!r}  ref {g!r}  exacta {exacta}  F1 {f:.2f}")

# sum() de booleanos = numero de aciertos; len(filas) = numero de casos
print("exactas:", sum(e for _, _, e, _ in filas), "de", len(filas))
print("F1 medio:", round(sum(f for _, _, _, f in filas) / len(filas), 3))
