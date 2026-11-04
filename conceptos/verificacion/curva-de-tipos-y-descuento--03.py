# --- inicio formula 3 ---
# Por que el mismo punto de tipos duele ocho veces mas a 10 anos que a 1: el cero.
def cero(z, t):
    # Bono cupon cero a t anos: un unico pago de 1.000 en t. El DF y el precio son lo mismo.
    return 1000.0 / (1 + z) ** t

z_actual, z_nuevo = 0.03, 0.04
for t in (1, 2, 5, 10):
    antes, despues = cero(z_actual, t), cero(z_nuevo, t)
    # El DF se imprime con el tipo viejo: es el valor de hoy de un euro, no del pago de 1.000.
    print("plazo %2d  DF %.4f  precio %8.2f  caida %6.2f %%"
          % (t, 1 / (1 + z_actual) ** t, antes, 100 * (despues / antes - 1)))
# --- fin formula 3 ---
# -> plazo  1  DF 0.9709  precio   970.87  caida  -0.96 %
# -> plazo  2  DF 0.9426  precio   942.60  caida  -1.91 %
# -> plazo  5  DF 0.8626  precio   862.61  caida  -4.72 %
# -> plazo 10  DF 0.7441  precio   744.09  caida  -9.21 %
