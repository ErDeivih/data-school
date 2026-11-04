# Por que el consumidor tiene que ser idempotente: la misma clave, dos entregas.
pedidos = {}
procesados = set()                  # set: la pertenencia es inmediata y no admite repetidos

def consumir(mensaje):
    clave = (mensaje["clave"], mensaje["version"])   # operacion + version, y tiene que ser tupla
    if clave in procesados:                          # esta es la comprobacion que da idempotencia
        return "duplicado ignorado"
    procesados.add(clave)
    pedidos[mensaje["pedido"]] = pedidos.get(mensaje["pedido"], 0) + 1
    # .get con 0 por defecto: la primera vez la clave no existe y un pedidos[...] daria KeyError
    return "procesado"

entrega = {"clave": "pedido-251", "version": 1, "pedido": 251}
print("primera entrega:", consumir(entrega))     # -> procesado
print("reintento:     ", consumir(entrega))      # -> duplicado ignorado
print("veces contabilizado el pedido 251:", pedidos[251])   # -> 1
print("mensajes vistos:", len(procesados))       # -> 1
