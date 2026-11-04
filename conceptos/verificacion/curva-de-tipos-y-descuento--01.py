# --- inicio formula 1 ---
# Valorar un bono con la curva entera, no con un tipo unico. La diferencia es el error que se comete.
plazos = [1, 2, 3, 4, 5]
tipos = [0.025, 0.028, 0.030, 0.032, 0.036]   # tipos al contado, uno por plazo
cupon, nominal = 30.0, 1000.0

# Un bono cupon cero tiene un solo flujo al final; con cupones, uno por ano y el nominal en el ultimo.
flujos = [cupon] * (len(plazos) - 1) + [cupon + nominal]
# El factor de descuento se calcula plazo a plazo: exponente entero, no interpolacion.
descuentos = [1 / (1 + z) ** t for t, z in zip(plazos, tipos)]
valores = [c * d for c, d in zip(flujos, descuentos)]
precio_curva = sum(valores)
# Con un unico tipo del 3 % el bono vale exactamente el nominal: el cupon coincide con el tipo.
precio_plano = sum(c / 1.03 ** t for t, c in zip(plazos, flujos))
# --- fin formula 1 ---

for t, z, d, v in zip(plazos, tipos, descuentos, valores):
    print("ano %2d  z %.3f  DF %.4f  VA %8.2f" % (t, z, d, v))
print("precio con la curva:  %.2f" % precio_curva)     # -> 974.61
print("precio con el 3 %%:    %.2f" % precio_plano)     # -> 1000.00
print("error por simplificar: %.2f %%" % (100 * (precio_plano / precio_curva - 1)))  # -> 2.60 %
