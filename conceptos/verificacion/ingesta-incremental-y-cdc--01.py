# El mismo cambio real aplicado con marca de tiempo y con CDC.
destino = {1: ("ana", "madrid"), 2: ("luis", "sevilla"), 3: ("marta", "bilbao")}
cambios = [("I", 4, ("pablo", "valencia")),
           ("U", 2, ("luis", "granada")),
           ("D", 3, None),
           ("U", 1, ("ana maria", "madrid"))]

# 1) Con updated_at, el borrado de la fila 3 no genera ninguna marca nueva que leer.
vistos_por_marca = [1, 2, 4]
print("filas que ve updated_at:", len(vistos_por_marca))   # -> filas que ve updated_at: 3
print("la fila 3 sigue en el destino:", 3 in destino)      # -> la fila 3 sigue en el destino: True

# 2) Con CDC, el log trae la operacion y el borrado tambien se aplica.
for op, clave, valor in cambios:
    if op == "D":
        destino.pop(clave, None)
    else:
        destino[clave] = valor

print("filas tras CDC:", len(destino))                     # -> filas tras CDC: 3
print("la fila 3 sigue en el destino:", 3 in destino)      # -> la fila 3 sigue en el destino: False
print("ciudad de la fila 2:", destino[2][1])               # -> ciudad de la fila 2: granada
