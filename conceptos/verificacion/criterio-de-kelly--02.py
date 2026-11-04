import numpy as np

# Version continua: con retornos normales la fraccion de Kelly es mu / sigma^2.
mu_mensual, sigma_mensual = 0.01, 0.04      # 1 % de exceso y 4 % de volatilidad al mes
f_kelly = mu_mensual / sigma_mensual ** 2

print(f"Kelly completo {f_kelly:.2f}x")                          # -> 6.25x
print(f"medio Kelly    {f_kelly / 2:.2f}x")                      # -> 3.12x
print(f"volatilidad anual al Kelly completo {f_kelly * sigma_mensual * np.sqrt(12):.2%}")
# -> 86.60%

# La cuota cambia la fraccion: con la misma probabilidad, pagar 2 por 1 permite mas.
p = 0.55
print(f"con cuota 2:1 la fraccion seria {p - (1 - p) / 2:.2f}")   # -> 0.33
