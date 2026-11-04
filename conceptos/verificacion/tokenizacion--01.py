from collections import Counter

# BPE minimo: fusiona el par de simbolos adyacentes mas frecuente del corpus.
corpus = {"baja": 5, "bajo": 3, "bajada": 2}

def piezas(p):
    return list(p[:-1]) + [p[-1] + "</w>"]      # </w> marca el fin de palabra

def contar(vocab):
    pares = Counter()                           # Counter devuelve 0 en una clave que no existe
    for pzas, n in vocab:
        for a, b in zip(pzas, pzas[1:]):        # empareja cada simbolo con el siguiente
            pares[(a, b)] += n                  # la clave es una TUPLA de dos simbolos
    return pares

vocab = [(piezas(p), n) for p, n in corpus.items()]
print("inicio:", vocab[0][0])                   # -> ['b', 'a', 'j', 'a</w>']

merges = []
for _ in range(4):
    # En caso de empate gana el par alfabeticamente menor: el criterio debe ser fijo.
    # El - delante de kv[1] ordena de mas a menos frecuente; str(kv[0]) desempata siempre igual.
    (a, b), n = sorted(contar(vocab).items(), key=lambda kv: (-kv[1], str(kv[0])))[0]
    merges.append((a + b, n))
    nuevo = []
    for pzas, cnt in vocab:
        salida, i = [], 0
        while i < len(pzas):
            if i < len(pzas) - 1 and pzas[i] == a and pzas[i + 1] == b:
                salida.append(a + b); i += 2    # una sola pasada: no se refusiona lo ya fusionado
            else:
                salida.append(pzas[i]); i += 1
        nuevo.append((salida, cnt))
    vocab = nuevo                               # se reasigna el nombre, no se toca la lista vieja

print("merges:", merges)
# -> [('aj', 10), ('baj', 10), ('baja</w>', 5), ('bajo</w>', 3)]
print("final :", [(cnt, pzas) for pzas, cnt in vocab])
# -> [(5, ['baja</w>']), (3, ['bajo</w>']), (2, ['baj', 'a', 'd', 'a</w>'])]
