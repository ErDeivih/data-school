# Buscar la clave candidata y los centinelas: las dos comprobaciones que evitan sorpresas.
columnas = {
    "pedido_id": [1, 2, 3, 4, 5, 6],
    "importe":   [120.5, 80.0, 45.25, None, 999999.0, 60.0],
    "alta":      ["2024-01-05", "2024-01-05", "2024-01-06",
                  "2024-01-07", "1900-01-01", "2024-01-08"],
}

# Candidata a clave: tantos valores distintos como filas y ningun hueco.
clave = [c for c, v in columnas.items() if len(set(v)) == len(v) and None not in v]
print("candidatas a clave:", clave)   # -> candidatas a clave: ['pedido_id']

# Un valor que se repite y no tiene sentido de negocio es un centinela disfrazado.
print("fecha 1900-01-01 repetida:", columnas["alta"].count("1900-01-01"))
# -> fecha 1900-01-01 repetida: 1

# Los huecos hay que quitarlos a mano: Python no compara None con un numero.
presentes = [v for v in columnas["importe"] if v is not None]
print("importe maximo:", max(presentes))   # -> importe maximo: 999999.0
