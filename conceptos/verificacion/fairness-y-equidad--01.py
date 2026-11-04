import numpy as np

# Mismo modelo en los dos grupos. Cada fila: [aciertos, falsos negativos, falsas alarmas, rechazos correctos]
a = np.array([286, 14, 111, 589])      # grupo A: 1.000 personas, 300 aptas de verdad
b = np.array([57, 3, 70, 370])         # grupo B:   500 personas,  60 aptas de verdad


def tasas(x):
    tp, fn, fp, tn = x
    return (tp + fp) / x.sum(), tp / (tp + fn), fp / (fp + tn)


sel_a, tpr_a, fpr_a = tasas(a)
sel_b, tpr_b, fpr_b = tasas(b)
print(f"tasa de seleccion  A {sel_a:.3f}  B {sel_b:.3f}  brecha {abs(sel_a - sel_b):.3f}")
print(f"exhaustividad      A {tpr_a:.3f}  B {tpr_b:.3f}  brecha {abs(tpr_a - tpr_b):.3f}")
print(f"falsas alarmas     A {fpr_a:.3f}  B {fpr_b:.3f}  brecha {abs(fpr_a - fpr_b):.3f}")
# -> tasa de seleccion  A 0.397  B 0.254  brecha 0.143
# -> exhaustividad      A 0.953  B 0.950  brecha 0.003
# -> falsas alarmas     A 0.159  B 0.159  brecha 0.001
