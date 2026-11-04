import numpy as np

y = np.array([1, 1, 1, 0, 0, 0, 0, 0])
score = np.array([0.95, 0.60, 0.40, 0.85, 0.55, 0.35, 0.20, 0.10])
# int(...) convierte los enteros de NumPy en enteros de Python: la division da lo mismo,
# pero evita que se cuelen tipos raros al imprimir o al guardar.
positivos, negativos = int((y == 1).sum()), int((y == 0).sum())

# Cada umbral es un clasificador distinto; la curva ROC es el rastro que dejan
for tau in (0.95, 0.85, 0.60, 0.40):
    pred = score >= tau
    # Los parentesis de cada comparacion son obligatorios: & se evalua antes que == y
    # pred == 1 & (y == 1) se calcularia al reves. Con arrays se usa &, nunca `and`.
    tpr = int(((pred == 1) & (y == 1)).sum()) / positivos
    fpr = int(((pred == 1) & (y == 0)).sum()) / negativos
    print(f"umbral {tau:.2f}  TPR {tpr:.3f}  FPR {fpr:.3f}")
# -> umbral 0.95  TPR 0.333  FPR 0.000
# -> umbral 0.85  TPR 0.333  FPR 0.200
# -> umbral 0.60  TPR 0.667  FPR 0.200
# -> umbral 0.40  TPR 1.000  FPR 0.400
