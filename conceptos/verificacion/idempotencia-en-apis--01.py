def crear_pedido(clave, lineas, cache):
    """Devuelve (respuesta, repetida). El cache hace de tabla con clave unica."""
    if clave in cache:                     # reintento: devolvemos la respuesta original
        return cache[clave], True
    # El identificador se deriva del numero de entradas del cache: en produccion lo asigna
    # la base de datos, no el codigo.
    respuesta = {"id": len(cache) + 1000, "total": sum(lineas)}
    cache[clave] = respuesta               # en produccion, en la misma transaccion
    return respuesta, False

cache = {}
# Cada llamada devuelve dos cosas: la respuesta y si era un reintento. En la tercera, el
# guion bajo descarta ese segundo valor porque no se va a usar.
primera, repetida = crear_pedido("k-1", [3.50, 6.50], cache)
segunda, repetida2 = crear_pedido("k-1", [3.50, 6.50], cache)
tercera, _ = crear_pedido("k-2", [1.00], cache)

print("primera llamada:", primera, "repetida:", repetida)      # -> repetida: False
print("mismo key      :", segunda, "repetida:", repetida2)     # -> el MISMO diccionario
print("otra key       :", tercera)
print("pedidos creados:", len(cache), "de 3 peticiones")       # -> 2 de 3
