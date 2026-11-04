import pandas as pd

# Cuarentena: el registro en crudo, el motivo y la tanda. Con eso se puede reprocesar.
cuarentena = pd.DataFrame({
    "pedido_id": ["P3", "P4", "P5"],
    "unidades": [-3, 4, 0],
    "motivo": ["unidades no positivas", "precio vacio", "unidades no positivas"],
})
tabla = pd.DataFrame({"pedido_id": ["P1", "P2", "P6"], "unidades": [2, 1, 7]})

# Arreglada la causa, se reprocesa la cuarentena y la clave de destino evita duplicar.
arreglados = cuarentena.assign(unidades=[3, 4, 1])[["pedido_id", "unidades"]]
tabla = pd.concat([tabla, arreglados]).drop_duplicates(subset="pedido_id", keep="last")
print(tabla.sort_values("pedido_id").to_string(index=False))
print("filas tras el reproceso:", len(tabla))
# -> 6
