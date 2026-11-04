import pandas as pd

# Una sola tabla fisica y una politica por rol: que filas y que columnas ve cada uno.
ventas = pd.DataFrame({
    "pais": ["ES", "ES", "FR", "DE", "ES"],
    "comercial": ["ana", "luis", "ana", "luis", "ana"],
    "importe": [1000, 250, 4000, 150, 3200],
    "cliente": ["ACME", "PEREZ SL", "ACME", "GARCIA", "ACME"],
})

politicas = {
    "ana": {"filas": lambda d: d["pais"] == "ES",
            "columnas": ["pais", "comercial", "importe"]},
    "luis": {"filas": lambda d: d["comercial"] == "luis",
             "columnas": ["pais", "importe", "cliente"]},
}

def vista(df, usuario):
    p = politicas[usuario]
    return df[p["filas"](df)][p["columnas"]]

for usuario in politicas:
    v = vista(ventas, usuario)
    print(usuario, "ve", len(v), "filas y", len(v.columns), "columnas:", ", ".join(v.columns))
# -> ana ve 3 filas y 3 columnas: pais, comercial, importe
# -> luis ve 2 filas y 3 columnas: pais, importe, cliente

# La trampa: filtrar en la aplicacion DESPUES de limitar deja entrar filas de otro pais.
recortado = ventas.head(3)
print("filas de otro pais que se cuelan:", int((recortado["pais"] != "ES").sum()))
# -> 1
