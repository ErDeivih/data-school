# Grid 2 x 2 x 2 determinista: A = primer bit, B = segundo bit, C = "los bits son iguales".
casos = [(a, b) for a in (0, 1) for b in (0, 1)]      # 4 combinaciones equiprobables
n = len(casos)

P = lambda pred: sum(1 for c in casos if pred(*c)) / n

p_a = P(lambda a, b: a == 1)
p_b = P(lambda a, b: b == 1)
p_ab = P(lambda a, b: a == 1 and b == 1)
p_c = P(lambda a, b: a == b)
p_ab_c = P(lambda a, b: a == 1 and b == 1 and a == b) / p_c
p_a_c = P(lambda a, b: a == 1 and a == b) / p_c
p_b_c = P(lambda a, b: b == 1 and a == b) / p_c

print("P(A)             ", p_a)                # salida: 0.5
print("P(A y B)         ", p_ab)               # salida: 0.25
print("P(A)*P(B)        ", p_a * p_b)          # salida: 0.25  -> independientes
print("P(A y B dado C)  ", p_ab_c)             # salida: 0.5
print("P(A|C)*P(B|C)    ", p_a_c * p_b_c)      # salida: 0.25  -> no cond. independientes
