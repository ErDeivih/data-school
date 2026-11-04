# El modelo de tiempo por token cuando manda el ancho de banda: por que agrupar sale
# casi gratis y por que la cuantizacion acelera la generacion.
B_GB_S = 900.0               # ancho de banda de la tarjeta, GB/s
PESOS_16BITS = 13.04         # GiB de pesos
PESOS_4BITS = 3.26           # GiB de pesos
CACHE_POR_SECUENCIA = 1.95   # GiB con 4.000 tokens de contexto

def ms_por_token(pesos_gib, cache_gib, lotes=1):
    # Se leen los pesos una vez por paso (sirven para todo el lote) y la cache de cada
    # secuencia, que si se paga entera por secuencia.
    return (pesos_gib + cache_gib * lotes) / B_GB_S * 1000

for bits, pesos in (("16 bits", PESOS_16BITS), ("4 bits", PESOS_4BITS)):
    t = ms_por_token(pesos, 0.0)
    print(f"{bits}: {t:5.1f} ms por token -> {1000 / t:6.1f} tokens por segundo")
# -> 16 bits:  14.5 ms por token ->   69.0 tokens por segundo
# ->  4 bits:   3.6 ms por token ->  276.1 tokens por segundo

# El lote no multiplica el tiempo: los pesos se leen una vez y sirven para todos.
print("lote  tiempo_por_token  tokens_por_segundo_del_conjunto")
for lotes in (1, 2, 4, 8, 16):
    t = ms_por_token(PESOS_16BITS, CACHE_POR_SECUENCIA, lotes)
    print(f"{lotes:4d}  {t:15.1f}  {lotes * 1000 / t:28.1f}")
# -> lote  tiempo_por_token  tokens_por_segundo_del_conjunto
# ->    1             16.7                          60.0
# ->    2             18.8                         106.3
# ->    4             23.2                         172.7
# ->    8             31.8                         251.4
# ->   16             49.2                         325.5

# Y de donde sale la memoria que ocupa cada lote: la cache si se multiplica.
for lotes in (4, 8, 16):
    print(f"  lote {lotes:2d} -> {lotes * CACHE_POR_SECUENCIA:5.2f} GiB de cache")
# -> lote 4 ->  7.80 GiB de cache
# -> lote 8 -> 15.60 GiB de cache
# -> lote 16 -> 31.20 GiB de cache
# ojo: el lote 16 pide 31,20 GiB de cache y no cabe en una tarjeta de 24
