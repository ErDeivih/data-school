import pandas as pd

# El valor por defecto viene en la firma: how="inner". Comprobarlo cuesta una linea y
# evita suponer lo que hace la funcion cuando la clave esta repetida o falta.
izquierda = pd.DataFrame({"id": [1, 2, 3], "importe": [10.0, 20.0, 30.0]})
derecha = pd.DataFrame({"id": [1, 2, 4], "pais": ["ES", "FR", "IT"]})

print("inner por defecto:", izquierda.merge(derecha, on="id").shape[0])                 # -> 2
print("outer explicito :", izquierda.merge(derecha, on="id", how="outer").shape[0])     # -> 4
print("nulos del outer :", int(izquierda.merge(derecha, on="id", how="outer").isna().sum().sum()))  # -> 2

# La firma es el contrato: si falta un argumento obligatorio, Python avisa antes de tocar datos.
try:
    izquierda.merge()
except TypeError as error:
    print("sin argumentos  :", error)
