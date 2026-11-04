# Parametros de una convolucion frente a una capa densa sobre la misma entrada.
C_in, C_out, F = 3, 16, 3
conv = F * F * C_in * C_out + C_out
densa = (32 * 32 * C_in) * C_out + C_out
print("parametros conv :", conv)                 # -> 448
print("parametros densa:", densa)                # -> 49168
print("veces menos     :", round(densa / conv))  # -> 110

# Forma de salida con H=32, F=3, P=1 y dos pasos distintos.
print("S=1 ->", (32 + 2 * 1 - 3) // 1 + 1)   # -> 32
print("S=2 ->", (32 + 2 * 1 - 3) // 2 + 1)   # -> 16

# Campo receptivo de dos convoluciones 3x3 con paso 1: r = 1 + 2 + 2.
print("campo receptivo:", 1 + (3 - 1) + (3 - 1))   # -> 5
