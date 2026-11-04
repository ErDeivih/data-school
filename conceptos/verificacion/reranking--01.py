consulta = "cambiar la contrasena de acceso"

# Etapa 1: el bi-codificador ya vectorizo todo el corpus. Guardamos su puntuacion y la
# relevancia real de cada documento (3 = responde del todo, 0 = no responde).
candidatos = [
    ("A", 0.81, 2, "cambiar la contrasena de la cuenta"),
    ("B", 0.79, 1, "donde veo mi contrasena guardada"),
    ("C", 0.74, 3, "acceso a la cuenta y cambio de contrasena"),
    ("D", 0.72, 0, "recuperar la contrasena olvidada del correo"),
    ("E", 0.70, 2, "acceso desde el movil y datos personales"),
]

def pares(secuencia, n):
    # conjuntos de n-gramas: set(), para que una repeticion no cuente dos veces
    return set(tuple(secuencia[i:i + n]) for i in range(len(secuencia) - n + 1))

def codificador_cruzado(q, doc):
    # El codificador cruzado lee consulta y documento juntos: puede premiar frases exactas.
    p = doc.split()
    # suma palabras sueltas (peso 1), bigramas (2) y trigramas (3): cuanto mas larga la
    # coincidencia, mas pesa. La interseccion & de dos set() es la parte comun.
    return (sum(p.count(w) for w in q.split())
            + 2 * len(pares(q.split(), 2) & pares(p, 2))
            + 3 * len(pares(q.split(), 3) & pares(p, 3)))

etapa1 = [i for i, _, _, _ in sorted(candidatos, key=lambda c: -c[1])]
puntuaciones = {i: codificador_cruzado(consulta, t) for i, _, _, t in candidatos}
# sorted sobre un diccionario recorre sus CLAVES, y la clave es la funcion del orden
etapa2 = sorted(puntuaciones, key=lambda i: -puntuaciones[i])
relevancia = {i: r for i, _, r, _ in candidatos}

def mrr(orden):
    # la lista tiene que venir ya ordenada: la posicion es la del recorrido
    for posicion, i in enumerate(orden, 1):
        if relevancia[i] == 3:
            return 1.0 / posicion

print("etapa 1 (bi-codificador)", etapa1, " MRR", round(mrr(etapa1), 3))
print("etapa 2 (reordenacion)  ", etapa2, " MRR", round(mrr(etapa2), 3))
print("puntuaciones cruzadas", {i: puntuaciones[i] for i in etapa2})
print("top-3 antes", etapa1[:3], "despues", etapa2[:3])
# el documento C sube de la tercera a la segunda posicion solo por reordenar
