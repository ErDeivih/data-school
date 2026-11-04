import numpy as np

# Las mismas dos estrategias del principio: resultados parecidos, riesgo muy distinto.
suave = np.array([0.02, 0.01, 0.02, 0.01, 0.02, 0.01, 0.02, 0.01, 0.02, 0.01, 0.02, 0.01])
brusca = np.array([0.10, -0.08, 0.12, -0.07, 0.09, 0.06, 0.10, -0.09, 0.08, 0.05, 0.11, -0.19])


def resumen(x):
    c = np.cumprod(1 + x)
    picos = np.maximum.accumulate(c)
    return (c[-1] - 1), float(((picos - c) / picos).max()), x.std(ddof=1)


for nombre, x in (("suave ", suave), ("brusca", brusca)):
    total, mdd, vol = resumen(x)
    print(f"{nombre}  final {total:+.1%}  caida {mdd:>6.2%}  volatilidad {vol:.2%}")
# -> suave   final +19.5%  caida  0.00%  volatilidad 0.52%
# -> brusca  final +24.3%  caida 19.00%  volatilidad 10.27%
