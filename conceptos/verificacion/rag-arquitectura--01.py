import numpy as np

# Similitud coseno entre la consulta y cuatro fragmentos (vectores escritos a mano)
consulta = np.array([1.0, 0.0, 0.5])
fragmentos = {
    "A": np.array([1.0, 0.1, 0.4]),
    "B": np.array([0.2, 1.0, 0.1]),
    "C": np.array([0.9, 0.2, 0.6]),
    "D": np.array([0.0, 0.3, 0.9]),
}

def coseno(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))   # @ es el producto escalar; float() saca un escalar de Python

denso = sorted(fragmentos, key=lambda k: -coseno(consulta, fragmentos[k]))   # de mas parecido a menos: por eso el menos
lexico = ["D", "A", "B", "C"]          # orden que daria un buscador por palabras

# Fusion de rangos reciprocos (RRF): cada lista aporta 1 / (k + posicion)
k = 60
rrf = {c: 1 / (k + denso.index(c) + 1) + 1 / (k + lexico.index(c) + 1) for c in fragmentos}
for c in sorted(rrf, key=lambda x: -rrf[x]):     # ordena las claves del diccionario por su valor RRF
    print(f"{c}: denso {denso.index(c) + 1}  lexico {lexico.index(c) + 1}  RRF {rrf[c]:.5f}")
# -> A 0.03252, D 0.03227, C 0.03175, B 0.03150
