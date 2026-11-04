import numpy as np

# Volumen de pedidos de los cinco lunes anteriores y del lunes de hoy.
lunes_previos = np.array([1_180_000, 1_240_000, 1_210_000, 1_195_000, 1_225_000])
hoy = 430_000

mediana = np.median(lunes_previos)
mad = np.median(np.abs(lunes_previos - mediana))       # robusto: un extremo no lo mueve
z = 0.6745 * (hoy - mediana) / mad

print(f"mediana   {mediana:,.0f}")        # -> mediana   1,210,000
print(f"MAD       {mad:,.0f}")            # -> MAD       15,000
print(f"z robusto {z:.1f}")               # -> z robusto -35.1

# La misma formula con una caida del 5 %: no deberia disparar.
z_suave = 0.6745 * (0.95 * mediana - mediana) / mad
print(f"caida del 5 % -> z {z_suave:.2f}")   # -> caida del 5 % -> z -2.72
