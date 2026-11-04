PRECIO_GPU_HORA = 2.50
TOKENS_POR_SEGUNDO = 2000.0
HORAS_MES = 24 * 30
coste_gpu_mes = PRECIO_GPU_HORA * HORAS_MES

# Palanca 1: cuantizar sube los tokens por segundo del mismo hardware. Los factores son
# orientativos (dependen del modelo y de la GPU); lo que se comprueba aqui es la aritmetica.
for factor, etiqueta in ((1.0, "sin cuantizar"), (1.6, "int8"), (2.3, "int4")):
    tokens_mes = TOKENS_POR_SEGUNDO * factor * 3600 * HORAS_MES / 1e6
    coste = coste_gpu_mes / tokens_mes
    print(f"{etiqueta:14s} {factor:4.1f}x tokens/segundo -> {coste:.4f} EUR por millon al 100%")
# -> sin cuantizar  1.0x tokens/segundo -> 0.3472 EUR por millon al 100%
# -> int8           1.6x tokens/segundo -> 0.2170 EUR por millon al 100%
# -> int4           2.3x tokens/segundo -> 0.1510 EUR por millon al 100%

# Palanca 2: el coste por millon no depende del PRECIO de la hora, depende de la utilizacion.
for precio_hora in (1.00, 2.50, 5.00):
    lleno = (precio_hora * HORAS_MES) / (TOKENS_POR_SEGUNDO * 3600 * HORAS_MES / 1e6)
    print(f"GPU a {precio_hora:4.2f} EUR/h -> coste lleno {lleno:.4f} EUR/M"
          f"   equilibrio contra 3.00 EUR/M: {3.00 / lleno:.2%}")
# -> GPU a 1.00 EUR/h -> coste lleno 0.1389 EUR/M   equilibrio contra 3.00 EUR/M: 2160.00%
# -> GPU a 2.50 EUR/h -> coste lleno 0.3472 EUR/M   equilibrio contra 3.00 EUR/M: 864.00%
# -> GPU a 5.00 EUR/h -> coste lleno 0.6944 EUR/M   equilibrio contra 3.00 EUR/M: 432.00%
