import numpy as np

# El mismo ajuste, en corto, para ver que un evento nuevo reescribe TODO el pasado.
bruto = np.array([100.0, 102.0, 103.0, 100.0, 50.0, 52.0, 55.0])

# Antes del dividendo: solo hay un split 1:2 en la posicion 4 (ratio 50/100).
factor_previo = np.ones(len(bruto))
factor_previo[:4] = bruto[4] / bruto[3]        # 0,5: el pasado se pone en la base nueva
enero_previo = bruto[0] * factor_previo[0]

# Se anuncia un dividendo de 1,0 en la posicion 6 y se recalcula todo hacia atras.
factor_nuevo = np.ones(len(bruto))
factor_nuevo[:6] = (bruto[6] + 1.0) / bruto[5]     # el dividendo, (55 + 1) / 52
factor_nuevo[:4] *= bruto[4] / bruto[3]            # y por debajo sigue estando el split
enero_nuevo = bruto[0] * factor_nuevo[0]

print(round(enero_previo, 4))                  # -> 50.0
print(round(enero_nuevo, 4))                   # -> 53.8462
print(round(enero_nuevo - enero_previo, 4))    # -> 3.8462

# El factor no es constante: no se puede deshacer el ajuste dividiendo por un solo numero.
print(round(float(factor_nuevo[1]), 5), round(float(factor_nuevo[5]), 5))  # -> 0.53846 1.07692
print(round(float(np.unique(np.round(factor_nuevo, 5)).size), 0))          # -> 3.0
