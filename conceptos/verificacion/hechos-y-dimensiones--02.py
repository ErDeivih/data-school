# Clave sustituta frente a clave natural, y el miembro desconocido
ORIGEN = [{"codigo": "TEC-01", "unidades": 2},
          {"codigo": "RAT-02", "unidades": 1},
          {"codigo": "MON-03", "unidades": 5}]       # este producto no esta en la dimension

DIM_PRODUCTO = [(-1, "DESCONOCIDO", "Desconocido"),
                (1, "TEC-01", "teclado"),
                (2, "RAT-02", "raton")]

por_codigo = {natural: (sustituta, nombre) for sustituta, natural, nombre in DIM_PRODUCTO}
hechos = []
for fila in ORIGEN:
    sustituta, nombre = por_codigo.get(fila["codigo"], (-1, "Desconocido"))
    hechos.append({"codigo_natural": fila["codigo"], "producto_id": sustituta,
                   "nombre": nombre, "unidades": fila["unidades"]})

print("codigo_natural  producto_id      nombre  unidades")
for h in hechos:
    print(f"{h['codigo_natural']:>14}  {h['producto_id']:>11}  {h['nombre']:>11}  {h['unidades']:>8}")

huerfanas = sum(h["unidades"] for h in hechos if h["producto_id"] == -1)
print("filas sin resolver:", sum(1 for h in hechos if h["producto_id"] == -1))   # -> 1
print("unidades huerfanas:", huerfanas)                                        # -> 5
