# --- inicio formula 2 ---
# Lo mismo con una subida de un punto en toda la curva: el error no es lineal.
flujos = [30.0, 30.0, 30.0, 30.0, 1030.0]

def precio(tipos, flujos):
    # Descuenta cada flujo con SU tipo: es lo unico que distingue la curva del tipo unico.
    return sum(c / (1 + z) ** (i + 1) for i, (c, z) in enumerate(zip(flujos, tipos)))

base = [0.025, 0.028, 0.030, 0.032, 0.036]
subida = [z + 0.01 for z in base]
# --- fin formula 2 ---

print("antes   %.2f" % precio(base, flujos))    # -> 974.61
print("despues %.2f" % precio(subida, flujos))  # -> 931.53
print("caida   %.2f %%" % (100 * (precio(subida, flujos) / precio(base, flujos) - 1)))  # -> -4.42 %
# La duracion de Macaulay del bono con la curva es 4,71 anos, luego D_mod = 4,55: la aproximacion
# lineal -4,55 % se queda algo larga frente al -4,42 % real. Esa curvatura es la convexidad.
