# Memoria de la cache KV: 2 (claves y valores) * capas * cabezas * dimension * tokens * bytes
def cache_mib(tokens, capas=32, cabezas=8, dim=128, bytes_por_valor=2):
    return 2 * capas * cabezas * dim * tokens * bytes_por_valor / 1024 ** 2   # 1024**2 pasa de bytes a MiB

for tokens in (4096, 8192, 32768):
    print(f"{tokens:>6} tokens -> {cache_mib(tokens):8.1f} MiB por secuencia")
# -> 256.0, 512.0 y 2048.0 MiB

# Y esa memoria se multiplica por el numero de peticiones simultaneas
print(f"32 secuencias de 8192 tokens: {cache_mib(8192) * 32 / 1024:.1f} GiB")   # -> 16.0 GiB
