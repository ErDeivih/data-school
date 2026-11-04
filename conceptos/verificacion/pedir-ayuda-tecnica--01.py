import pandas as pd

# Lo que ve el pipeline: una columna de importes que llega como texto con coma decimal.
importes = pd.Series(["10,50", "20,00", "sin dato"])
try:
    importes.astype(float)
except ValueError as error:
    print(f"error del pipeline: {error}")
# -> error del pipeline: could not convert string to float: '10,50'

# El ejemplo minimo: una sola llamada, sin ficheros ni base de datos de por medio.
# Deja ver que la causa no es el nulo, es la coma.
print(f"to_numeric('10,50') -> {pd.to_numeric('10,50', errors='coerce')}")   # -> nan
print(f"to_numeric('10.50') -> {pd.to_numeric('10.50', errors='coerce')}")   # -> 10.5
