import pandas as pd

izq = pd.DataFrame({"pedido": [1, 2, 3], "cliente": ["A", "A", "B"]})
der = pd.DataFrame({"cliente": ["A", "A", "B"], "descuento": [0.1, 0.2, 0.3]})

print(len(izq), len(der))                          # -> 3 3
print(len(izq.merge(der, on="cliente")))           # -> 5   (2*2 + 1*1: la clave de la derecha se repite)

# validate convierte el error silencioso en una excepcion explicita
try:
    izq.merge(der, on="cliente", validate="many_to_one")
    print("sin error")
except Exception as e:
    print(type(e).__name__)                        # -> MergeError

# indicator dice de donde vino cada fila, sin adivinar
unida = izq.merge(der, on="cliente", how="outer", indicator=True)
print(int((unida["_merge"] == "both").sum()))      # -> 5
