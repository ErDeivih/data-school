# Todos los numeros de la pagina salen de estas seis constantes.
PRECIO_GPU_HORA = 2.50          # alquiler de una GPU por hora, bajo demanda
TOKENS_POR_SEGUNDO = 2000.0     # tokens de salida por segundo con un lote razonable
HORAS_MES = 24 * 30

capacidad_mes = TOKENS_POR_SEGUNDO * 3600 * HORAS_MES / 1e6    # millones de tokens
coste_gpu_mes = PRECIO_GPU_HORA * HORAS_MES
coste_lleno = coste_gpu_mes / capacidad_mes                    # EUR por millon al 100 %

print(round(capacidad_mes, 1))          # -> 5184.0 millones de tokens al mes
print(round(coste_gpu_mes, 2))          # -> 1800.0 EUR al mes
print(round(coste_lleno, 4))            # -> 0.3472 EUR por millon con la GPU llena

# La utilizacion es el divisor: el mismo trabajo, repartido sobre mas o menos capacidad.
for utilizacion in (1.0, 0.6, 0.3, 0.2, 0.1, 0.05):
    print(f"utilizacion {utilizacion:5.0%}  ->  {coste_lleno / utilizacion:7.4f} EUR por millon")
# -> utilizacion  100%  ->   0.3472 EUR por millon
# -> utilizacion   60%  ->   0.5787 EUR por millon
# -> utilizacion   30%  ->   1.1574 EUR por millon
# -> utilizacion   20%  ->   1.7361 EUR por millon
# -> utilizacion   10%  ->   3.4722 EUR por millon
# -> utilizacion    5%  ->   6.9444 EUR por millon

# Cuanta utilizacion hace falta para empatar con cada precio de API.
for precio in (0.10, 0.50, 1.00, 3.00, 15.00):
    print(f"API {precio:6.2f} EUR/M  ->  utilizacion de equilibrio {precio / coste_lleno:.2%}")
# -> API   0.10 EUR/M  ->  utilizacion de equilibrio 28.80%
# -> API   0.50 EUR/M  ->  utilizacion de equilibrio 144.00%
# -> API   1.00 EUR/M  ->  utilizacion de equilibrio 288.00%
# -> API   3.00 EUR/M  ->  utilizacion de equilibrio 864.00%
# -> API  15.00 EUR/M  ->  utilizacion de equilibrio 4320.00%
