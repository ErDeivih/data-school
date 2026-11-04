import numpy as np

# Dos formas de calcular el MISMO producto escalar en float32: sumando en orden, uno a uno, o
# dejando que NumPy lo haga por parejas. Es lo que cambia entre dos motores de inferencia.
def suma_secuencial(x):
    total = np.float32(0.0)
    for v in x:
        total = np.float32(total + v)      # cada suma redondea a 24 bits de mantisa
    return float(total)

rng = np.random.default_rng(0)
for n in (1024, 4096, 16384):
    a = rng.normal(0, 1, n).astype(np.float32)
    b = rng.normal(0, 1, n).astype(np.float32)
    secuencial = suma_secuencial(a * b)
    por_parejas = float(np.dot(a, b))
    rel = abs(secuencial - por_parejas) / abs(por_parejas)
    print(f"n={n:6d}  secuencial={secuencial:+.7f}  numpy={por_parejas:+.7f}  error={rel:.2e}")
# -> n=  1024  secuencial=-83.3684998  numpy=-83.3685760  error=9.15e-07
# -> n=  4096  secuencial=+2.0263340  numpy=+2.0263424  error=4.12e-06
# -> n= 16384  secuencial=+40.7600327  numpy=+40.7601547  error=2.99e-06

# La unidad de redondeo NO es la misma en todo el rango: crece con el tamano del numero.
for v in (1.0, 1000.0, 1e6):
    print(v, float(np.spacing(np.float32(v))))
# -> 1.0 1.1920928955078125e-07
# -> 1000.0 6.103515625e-05
# -> 1000000.0 0.0625

# Validar un export: con igualdad falla, con tolerancia pasa.
referencia = rng.normal(0, 1, 5)
exportado = referencia + rng.normal(0, 1e-5, 5)
print(np.array_equal(referencia, exportado))                      # -> False
print(np.allclose(referencia, exportado, rtol=1e-4, atol=1e-5))   # -> True
