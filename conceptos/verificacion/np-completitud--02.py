from itertools import product

def evaluar(clausulas, asignacion):
    """Una clausula es una tupla de literales; el literal i>0 es x_i y i<0 es not x_i."""
    for clausula in clausulas:
        if not any((asignacion[abs(lit) - 1] if lit > 0 else not asignacion[abs(lit) - 1])
                   for lit in clausula):
            return False
    return True

def sat_bruto(clausulas, n_variables):
    """Busca la asignacion satisfactoria probando las 2^n posibilidades."""
    probadas = 0
    for bits in product([False, True], repeat=n_variables):
        probadas += 1
        if evaluar(clausulas, bits):
            return bits, probadas
    return None, probadas

# (x1 or x2 or x3) and (not x1 or not x2 or x3)
clausulas = [(1, 2, 3), (-1, -2, 3)]
asignacion, probadas = sat_bruto(clausulas, 3)
print("asignacion:", asignacion)              # -> asignacion: (False, False, True)
print("probadas:", probadas, "de", 2 ** 3)    # -> probadas: 2 de 8
print("todas ciertas:", evaluar(clausulas, asignacion))   # -> todas ciertas: True
