import numpy as np

# Dos estrategias que acaban el ano igual (+20 %) con caminos muy distintos.
suave = np.array([100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120], dtype=float)
brusca = np.array([100, 130, 128, 150, 120, 145, 118, 140, 112, 118, 120], dtype=float)

def caida_maxima(curva):
    picos = np.maximum.accumulate(curva)
    return float(((picos - curva) / picos).max())

print(f"suave   final {suave[-1] / suave[0] - 1:+.0%}   caida {caida_maxima(suave):.2%}")
# -> suave   final +20%   caida 0.00%
print(f"brusca  final {brusca[-1] / brusca[0] - 1:+.0%}   caida {caida_maxima(brusca):.2%}")
# -> brusca  final +20%   caida 25.33%
# Bajar de 150 a 112 y volver arriba cuesta mas de lo que sugiere el 25 % de caida.
print(f"la brusca necesita {(150 / 112 - 1):+.2%} para volver al pico")
# -> la brusca necesita +33.93% para volver al pico
