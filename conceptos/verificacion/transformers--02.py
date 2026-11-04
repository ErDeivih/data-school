# Contabilidad de un bloque transformer con d_model=512, 8 cabezas y d_ff=2048.
d_model, h, d_ff = 512, 8, 2048
qkvo = 4 * d_model * d_model        # W_Q, W_K, W_V y W_O
ffn = 2 * d_model * d_ff           # las dos lineales de la red hacia delante
normas = 2 * 2 * d_model           # dos LayerNorm, cada uno con escala y sesgo
# // es division entera: la dimension de cada cabeza tiene que ser exacta.
print("d_k por cabeza:", d_model // h)          # -> 64
print("atencion      :", qkvo)                  # -> 1048576
print("FFN           :", ffn)                   # -> 2097152
print("bloque entero :", qkvo + ffn + normas)   # -> 3147776

# Atencion y FFN cuestan lo mismo cuando n = d_ff.
print("n de cruce    :", d_ff)                  # -> 2048

# Memoria de la matriz de atencion, 8 cabezas, float32, por capa.
# 2**20 es un mebibyte en bytes (1.048.576); con 1e6 los numeros salen un 5 % mayores.
print(f"n= 512: {8 * 512 * 512 * 4 / 2**20:>6.1f} MiB")     # ->    8.0 MiB
print(f"n=1024: {8 * 1024 * 1024 * 4 / 2**20:>6.1f} MiB")   # ->   32.0 MiB
print(f"n=2048: {8 * 2048 * 2048 * 4 / 2**20:>6.1f} MiB")   # ->  128.0 MiB
