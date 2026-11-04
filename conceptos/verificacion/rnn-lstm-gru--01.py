# BPTT multiplica un factor por cada paso hacia atras: el producto decide todo.
# .3e es notacion cientifica con tres decimales: con .3f los dos ultimos casos saldrian
# 0.000 y no se veria ni que uno se apaga ni que el otro explota.
print(f"0.25^50 = {0.25 ** 50:.3e}")   # -> 7.889e-31  (desvanecido)
print(f"0.90^50 = {0.90 ** 50:.3e}")   # -> 5.154e-03  (vivo)
print(f"1.50^50 = {1.50 ** 50:.3e}")   # -> 6.376e+08  (explosivo)
