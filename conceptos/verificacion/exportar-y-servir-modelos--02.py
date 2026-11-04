import numpy as np

# Cuantizar al exportar: el mismo bloque de pesos guardado con menos bits.
rng = np.random.default_rng(0)
W = rng.normal(0.0, 0.05, size=(128, 128))


def reconstruir(W, bits):
    """Cuantizacion simetrica por tensor, como la de un export a int8 o int4."""
    qmax = 2 ** (bits - 1) - 1
    escala = np.abs(W).max() / qmax            # la escala la fija el peso mas extremo
    return np.clip(np.round(W / escala), -qmax - 1, qmax) * escala


def error_relativo(reconstruido):
    return float(np.sqrt(((W - reconstruido) ** 2).mean()) / W.std())


print(f"float32 sin tocar       {error_relativo(W.astype(np.float32).astype(np.float64)):.6f}")
# -> 0.000000
print(f"float16                 {error_relativo(W.astype(np.float16).astype(np.float64)):.6f}")
# -> 0.000208
print(f"int8                    {error_relativo(reconstruir(W, 8)):.6f}")   # -> 0.009173
print(f"int4                    {error_relativo(reconstruir(W, 4)):.6f}")   # -> 0.166905
print(f"int3                    {error_relativo(reconstruir(W, 3)):.6f}")   # -> 0.390986

# El tamano del fichero si es lo unico que miras: 131 KB en float64, 65 KB en float32.
print(W.nbytes)                                # -> 131072
print(W.astype(np.float32).nbytes)             # -> 65536
