# Cuantos tokens ocupa una imagen segun como se trocee. La cuenta es cuadratica en el lado,
# y de ahi sale la regla practica: la resolucion se elige, no se hereda del escaner.
def parches(lado, troceado=16):
    import math
    n = math.ceil(lado / troceado)
    return n, n * n

print("lado  troceado  rejilla  tokens")
for lado in (224, 336, 448, 672, 1008):
    n, total = parches(lado)
    print(f"{lado:4d}  {16:8d}  {n:3d}x{n:<3d}  {total:6d}")
# ->  224        16   14x14      196
# ->  336        16   21x21      441
# ->  448        16   28x28      784
# ->  672        16   42x42     1764
# -> 1008        16   63x63     3969

# Con un parche mas grande hay menos tokens... y menos detalle por token.
print("mismo lado, distinto troceado:")
for troceado in (8, 16, 32):
    n, total = parches(1008, troceado)
    print(f"  parche de {troceado:2d} px -> {n:3d}x{n:<3d} = {total:6d} tokens")
# -> parche de  8 px -> 126x126   =  15876 tokens
# -> parche de 16 px ->  63x63    =   3969 tokens
# -> parche de 32 px ->  32x32    =   1024 tokens
