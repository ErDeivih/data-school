import pandas as pd

# Cada reintento lleva la misma clave: el consumidor la usa para no repetir el cobro.
# La clave es del mensaje ("m-77"), no de la entrega, que puede ocurrir varias veces.
entregas = pd.DataFrame({
    "entrega": [1, 2, 3, 4],
    "clave":   ["m-77", "m-31", "m-77", "m-40"],
    "importe": [10.0, 5.0, 10.0, 2.0],
})

ingenuo = entregas.importe.sum()                            # suma todas las entregas
# drop_duplicates("clave") deja la PRIMERA fila de cada clave y descarta las demas; por eso
# la entrega 3 (m-77) desaparece. Devuelve un DataFrame nuevo, no modifica "entregas".
dedup = entregas.drop_duplicates("clave").importe.sum()     # una por mensaje logico

print("entregas recibidas:", len(entregas))                 # len() cuenta FILAS, no columnas
print("mensajes distintos:", entregas.clave.nunique())      # nunique() cuenta valores unicos
print("suma sin deduplicar:", f"{ingenuo:.2f}")
print("suma correcta     :", f"{dedup:.2f}")
