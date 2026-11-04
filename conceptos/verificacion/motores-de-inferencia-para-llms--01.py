# Cuanto ocupa un modelo y cuantas secuencias caben: la cuenta que decide si el servicio
# es viable antes de escribir una linea de codigo.
M_GPU = 24.0                 # GiB de la tarjeta
N_PARAMETROS = 7.0e9         # 7.000 millones de parametros
BYTES_POR_GB = 1024 ** 3

# Pesos del modelo: parametros por bits dividido entre 8. La tabla de escalas de la
# cuantizacion anade un poco, pero es un porcentaje pequeno y se deja fuera del calculo.
for bits in (32, 16, 8, 4):
    gb = N_PARAMETROS * bits / 8 / BYTES_POR_GB
    print(f"{bits:2d} bits -> {gb:6.2f} GiB de pesos   "
          f"{'cabe' if gb < M_GPU else 'NO CABE en la tarjeta'}")
# -> 32 bits ->  26.08 GiB de pesos   NO CABE en la tarjeta
# -> 16 bits ->  13.04 GiB de pesos   cabe
# ->  8 bits ->   6.52 GiB de pesos   cabe
# ->  4 bits ->   3.26 GiB de pesos   cabe

# La cache de claves crece con el contexto y con el numero de secuencias simultaneas.
# Modelo con 32 capas de atencion y dimension de cabeza de 128.
def cache_gb(segundos_contexto_tokens, bits_kv=16, lotes=1, capas=32, dim_cabeza=128, cabezas=32):
    bytes_por_token = 2 * capas * cabezas * dim_cabeza * bits_kv / 8
    return segundos_contexto_tokens * bytes_por_token * lotes / BYTES_POR_GB

for contexto in (4_000, 16_000, 32_000):
    print(f"contexto {contexto:6d} -> cache de {cache_gb(contexto):5.2f} GiB por secuencia")
# -> contexto   4000 -> cache de  1.95 GiB por secuencia
# -> contexto  16000 -> cache de  7.81 GiB por secuencia
# -> contexto  32000 -> cache de 15.62 GiB por secuencia

# Cuantas secuencias caben: el margen que queda despues de pesos, activaciones y reserva.
ACTIVACIONES = 2.0
for bits in (16, 8, 4):
    pesos = N_PARAMETROS * bits / 8 / BYTES_POR_GB
    margen = M_GPU - pesos - ACTIVACIONES
    for contexto in (4_000, 16_000):
        caben = int(margen / cache_gb(contexto))
        print(f"{bits:2d} bits, contexto {contexto:6d} -> margen {margen:5.2f} GiB, "
              f"caben {caben} secuencias")
# -> 16 bits, contexto   4000 -> margen  8.96 GiB, caben 4 secuencias
# -> 16 bits, contexto  16000 -> margen  8.96 GiB, caben 1 secuencias
# ->  8 bits, contexto   4000 -> margen 15.48 GiB, caben 7 secuencias
# ->  8 bits, contexto  16000 -> margen 15.48 GiB, caben 1 secuencias
# ->  4 bits, contexto   4000 -> margen 18.74 GiB, caben 9 secuencias
# ->  4 bits, contexto  16000 -> margen 18.74 GiB, caben 2 secuencias
