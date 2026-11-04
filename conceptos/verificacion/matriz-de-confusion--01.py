# 200 pacientes: 40 enfermos. El test detecta 34 y da 12 falsas alarmas.
# Cada caso es una pareja (real, predicho) con 1 = positivo; contar es construir la matriz.
# [(1, 1)] * 34 repite la MISMA tupla 34 veces. Con tuplas da igual porque son inmutables,
# pero con listas, [[0, 0]] * 3 deja tres filas enlazadas y cambiar una cambia las tres.
casos = [(1, 1)] * 34 + [(1, 0)] * 6 + [(0, 1)] * 12 + [(0, 0)] * 148

# sum(1 for ...) es una expresion generadora: recorre y suma sin construir una lista
# intermedia en memoria, que con un millon de casos se nota.
vp = sum(1 for real, pred in casos if real == 1 and pred == 1)
fn = sum(1 for real, pred in casos if real == 1 and pred == 0)
fp = sum(1 for real, pred in casos if real == 0 and pred == 1)
vn = sum(1 for real, pred in casos if real == 0 and pred == 0)

# En Python 3, vp / (vp + fn) es una division real aunque los dos sean enteros: da 0.85.
print(f"VP {vp}  FN {fn}  FP {fp}  VN {vn}")       # -> VP 34  FN 6  FP 12  VN 148
print(f"sensibilidad {vp / (vp + fn):.3f}")        # -> 0.850
print(f"especificidad {vn / (vn + fp):.3f}")       # -> 0.925
print(f"precision    {vp / (vp + fp):.3f}")        # -> 0.739
print(f"suma de la matriz {vp + fn + fp + vn}")    # -> 200

# sklearn.metrics.confusion_matrix devuelve esta misma tabla como array 2x2, con las
# filas = clase real y las columnas = clase predicha: con labels=[0, 1], [[VN, FP], [FN, VP]].
