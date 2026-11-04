PRECIO_GPU_HORA = 2.50
TOKENS_POR_SEGUNDO = 2000.0
HORAS_MES = 24 * 30
capacidad_mes = TOKENS_POR_SEGUNDO * 3600 * HORAS_MES / 1e6
coste_gpu_mes = PRECIO_GPU_HORA * HORAS_MES

# Escenario: 20 millones de tokens al dia y picos de diez veces la media.
MEDIA_DIARIA = 20.0
DEMANDA_MES = MEDIA_DIARIA * 30
PICO_SOBRE_MEDIA = 10.0

gpus = DEMANDA_MES / capacidad_mes * PICO_SOBRE_MEDIA
print(round(gpus, 3))                     # -> 1.157 GPUs para aguantar el pico

# En la practica se compran 2: no se alquilan fracciones y hace falta margen. Eso no cambia la
# utilizacion; lo que la cambiaria es que la demanda subiera.
utilizacion = DEMANDA_MES / (capacidad_mes * gpus)
print(f"{utilizacion:.2%}")              # -> 10.00%

# La factura mensual de cada opcion, con los mismos 600 millones de tokens.
for precio in (0.50, 1.00, 3.00, 15.00):
    print(f"API {precio:6.2f} EUR/M  ->  {DEMANDA_MES * precio:9,.0f} EUR al mes")
print(f"propio, 1 GPU            ->  {coste_gpu_mes:9,.0f} EUR al mes")
print(f"propio, 2 GPUs (pico)    ->  {coste_gpu_mes * 2:9,.0f} EUR al mes")
# -> API   0.50 EUR/M  ->        300 EUR al mes
# -> API   1.00 EUR/M  ->        600 EUR al mes
# -> API   3.00 EUR/M  ->      1,800 EUR al mes
# -> API  15.00 EUR/M  ->      9,000 EUR al mes
# -> propio, 1 GPU            ->      1,800 EUR al mes
# -> propio, 2 GPUs (pico)    ->      3,600 EUR al mes

# Los picos SON la utilizacion: la utilizacion de equilibrio es 1 / (pico sobre media).
print(1 / PICO_SOBRE_MEDIA)               # -> 0.1
print(1 / 3.0)                            # -> 0.3333... (con picos de solo 3x)
