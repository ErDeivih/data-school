import numpy as np

p, q = 0.55, 0.45            # probabilidad de ganar y de perder, pago 1:1

def ruina(riesgo_por_operacion):
    """Capital medido en unidades de riesgo: N = 1 / riesgo."""
    return (q / p) ** (1 / riesgo_por_operacion)

for r in (0.01, 0.02, 0.05, 0.10, 0.20):
    print(f"riesgo {r:>5.0%}  unidades {1 / r:>4.0f}  ruina {ruina(r):.2e}")
# -> riesgo    2%  unidades   50  ruina 4.39e-05
# -> riesgo   10%  unidades   10  ruina 1.34e-01

print(f"el 10% arriesga {ruina(0.10) / ruina(0.02):.0f} veces mas que el 2%")   # -> 3062
