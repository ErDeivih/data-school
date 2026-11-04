# 100 estudiantes. E = aprueba Estadística (50), P = aprueba Programación (40).
# La intersección son los índices 0-19 (20 estudiantes que aprueban las dos).
estadistica = set(range(0, 20)) | set(range(50, 80))
programacion = set(range(0, 20)) | set(range(80, 100))

p_e = len(estadistica) / 100
p_p = len(programacion) / 100
p_interseccion = len(estadistica & programacion) / 100
p_union = len(estadistica | programacion) / 100

print("P(E)             ", p_e)                                # salida: 0.5
print("P(P)             ", p_p)                                # salida: 0.4
print("P(E y P)         ", p_interseccion)                     # salida: 0.2
print("P(E o P)         ", p_union)                            # salida: 0.7
print("sumar sin restar ", p_e + p_p)                          # salida: 0.9
print("regla de la suma ", round(p_e + p_p - p_interseccion, 10))  # salida: 0.7
