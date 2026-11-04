pedido = {"estado": "pendiente", "version": 1}

def get(recurso):                       # GET no cambia nada
    return recurso["estado"], recurso["version"]      # devuelve una tupla (estado, version)

def put(recurso, estado):               # PUT es idempotente: mismo cuerpo, mismo resultado
    if recurso["estado"] != estado:     # solo sube la version si el estado cambia de verdad
        recurso["estado"] = estado
        recurso["version"] += 1
    return recurso["estado"], recurso["version"]

def delete(recurso):                    # DELETE es idempotente: la segunda vez tampoco pasa nada
    if recurso["estado"] != "cancelado":
        recurso["estado"] = "cancelado"
        recurso["version"] += 1
    return 204                          # un codigo, no un cuerpo: DELETE no devuelve nada

print("GET   x2 ->", get(pedido), get(pedido))          # -> ('pendiente', 1) ('pendiente', 1)
print("PUT   x2 ->", put(pedido, "enviado"), put(pedido, "enviado"))   # -> ('enviado', 2) ('enviado', 2)
print("DELETE x2 ->", delete(pedido), delete(pedido))   # -> 204 204
print("version final:", pedido["version"])              # -> 3 (la subio el PUT y la subio el DELETE)
