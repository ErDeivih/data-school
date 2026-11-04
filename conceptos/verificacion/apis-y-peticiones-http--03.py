# Que codigos merecen otro intento: la decision, escrita una sola vez
reintentables = {429, 500, 502, 503, 504}

def politica(codigo, intento, retry_after=None):
    if codigo in reintentables:
        return retry_after if retry_after is not None else min(30.0, 0.5 * 2 ** intento)
    return None                      # 4xx que no sea 429: reintentar no arregla nada

for codigo in (200, 401, 404, 429, 503):
    print(f"{codigo}: esperar {politica(codigo, 0)}")
