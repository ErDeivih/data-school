# Modelo de latencia: los parametros ya estan en milisegundos por token.
# Los tres primeros argumentos son obligatorios (entrada, salida y tokens ya en cache);
# los que llevan valor por defecto son los t0, a, a_c y b de la formula de latencia.
def latencia(entrada, salida, cache_aciertos, ttft_base=50.0, ms_por_token_entrada=0.002,
             ms_por_token_cache=0.0002, ms_por_token_salida=20.0):
    # El primer token espera a que se procese toda la entrada; los demas salen a ritmo de salida.
    ttft = (ttft_base + (entrada - cache_aciertos) * ms_por_token_entrada
            + cache_aciertos * ms_por_token_cache)
    # devuelve DOS numeros en una tupla: quien llame tiene que desempaquetarlos
    return ttft, ttft + salida * ms_por_token_salida

# cada caso es una tupla (nombre, tokens de entrada, tokens servidos desde cache)
casos = [("contexto corto", 4000, 0), ("contexto largo", 120000, 0),
         ("contexto largo con cache", 120000, 115000)]
for nombre, entrada, cache in casos:
    ttft, total = latencia(entrada, 300, cache)   # 300 es la salida, igual en los tres casos
    print(f"{nombre:26s} primer token {ttft:>7.0f} ms   total {total:>7.0f} ms")
# el total lo domina la salida; la cache solo mueve el primer token
