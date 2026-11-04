import math

# Los tres crecimientos clasicos, con numeros en vez de dibujos.
print("n".rjust(8), "n*log2(n)".rjust(12), "n^2".rjust(16), "n^2/(n*log2 n)".rjust(17))
for n in (100, 1000, 10000, 100000):
    print(f"{n:>8d} {n * math.log2(n):>12.0f} {n * n:>16d} {n / math.log2(n):>17.1f}")

# Duplicar la entrada cuesta una comparacion mas en la busqueda binaria:
print("2^19 elementos:", math.ceil(math.log2(2 ** 19)), "comparaciones")  # -> 2^19 elementos: 19 comparaciones
print("2^20 elementos:", math.ceil(math.log2(2 ** 20)), "comparaciones")  # -> 2^20 elementos: 20 comparaciones
