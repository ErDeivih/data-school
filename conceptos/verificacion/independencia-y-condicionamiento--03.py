import itertools

# Paradoja de Berkson: dos enfermedades independientes que dejan de serlo al condicionar
# en el ingreso, que es consecuencia de cualquiera de las dos.
p_enfermedad = 0.10
filas = []
for a, b in itertools.product([0, 1], [0, 1]):
    p = (p_enfermedad if a else 1 - p_enfermedad) * (p_enfermedad if b else 1 - p_enfermedad)
    filas.append((a, b, p))                  # (tiene A, tiene B, probabilidad conjunta)

p_ingreso = sum(p for a, b, p in filas if a or b)
p_a_dado_ingreso = sum(p for a, b, p in filas if a) / p_ingreso
p_ab_dado_ingreso = sum(p for a, b, p in filas if a and b) / p_ingreso

print("P(ingreso)        ", round(p_ingreso, 4))                 # salida: 0.19
print("P(A y B | ingreso)", round(p_ab_dado_ingreso, 4))        # salida: 0.0526
print("P(A|ing)*P(B|ing)", round(p_a_dado_ingreso**2, 4))       # salida: 0.277
print("son independientes:", bool(abs(p_ab_dado_ingreso - p_a_dado_ingreso**2) < 1e-9))  # salida: False
