# Regla de la suma con tres sucesos: inclusion-exclusion completa.
A = set(range(0, 50))        # P(A) = 0.50
B = set(range(25, 75))       # P(B) = 0.50
C = set(range(0, 100, 4))    # P(C) = 0.25

p = lambda s: len(s) / 100
union = p(A | B | C)
suma_simple = p(A) + p(B) + p(C)
inclusion_exclusion = suma_simple - p(A & B) - p(A & C) - p(B & C) + p(A & B & C)

print("P(A o B o C)          ", union)                          # salida: 0.81
print("A y B independientes  ", bool(abs(p(A & B) - p(A) * p(B)) < 1e-12))  # salida: True
print("suma de los tres      ", round(suma_simple, 4))          # salida: 1.25
print("suma - parejas        ", round(suma_simple - p(A & B) - p(A & C) - p(B & C), 4))  # salida: 0.75
print("inclusion-exclusion   ", round(inclusion_exclusion, 10))  # salida: 0.81
print("interseccion triple   ", round(p(A & B & C), 4))         # salida: 0.06
