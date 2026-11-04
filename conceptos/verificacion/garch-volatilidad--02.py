import numpy as np

omega, alpha, beta = 1e-5, 0.12, 0.86
larga = omega / (1 - alpha - beta)
print("persistencia %.2f" % (alpha + beta))                                  # -> 0.98
print("varianza de largo plazo %.6f  vol diaria %.2f%%" % (larga, 100 * np.sqrt(larga)))  # -> 2.24%
print("volatilidad anualizada %.1f%%" % (100 * np.sqrt(larga * 252)))        # -> 35.5%
print("vida media de un shock en dias %.1f" % (np.log(0.5) / np.log(alpha + beta)))       # -> 34.3

var_ayer = 0.0004                                # la varianza de ayer: 2% diario
for shock in (0.03, 0.05):                       # dos shocks distintos hoy
    v = omega + alpha * shock ** 2 + beta * var_ayer
    print("shock %.0f%%  varianza manana %.6f  vol diaria %.2f%%" % (100 * shock, v, 100 * np.sqrt(v)))
# -> shock 3%: varianza 0.000462 y vol 2.15%   shock 5%: varianza 0.000654 y vol 2.56%
