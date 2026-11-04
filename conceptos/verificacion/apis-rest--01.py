ids = list(range(1, 251))          # 250 pedidos
LIMITE_MAX = 100
offset, total_peticiones = 0, 0

while offset < len(ids):
    pedir = min(100, len(ids) - offset)      # la ultima pagina pide 50, no 100
    if pedir > LIMITE_MAX:
        raise ValueError("422: limite fuera de rango")    # el servidor no sirve 1000: corta
    pagina = ids[offset:offset + pedir]      # rebanada semiabierta: entra el offset, no el final
    total_peticiones += 1
    print(f"GET /v1/pedidos?limite={pedir}&offset={offset} -> {len(pagina):>3} items, "
          # :>3 es un ancho minimo de 3 alineado a la derecha: la columna cuadra al leerla
          f"desde el id {pagina[0]} hasta el {pagina[-1]}")
    offset += pedir

print("peticiones necesarias:", total_peticiones)   # -> 3
