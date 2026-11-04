import pandas as pd

# Agregado historico por cliente: cada fila usa solo lo anterior de ese cliente.
df = pd.DataFrame({
    "cliente": ["A", "A", "A", "B", "B", "B"],
    "importe": [10, 30, 20, 5, 5, 45],
})
df["media_previa"] = df.groupby("cliente")["importe"].transform(lambda s: s.shift().expanding().mean())

# La primera fila de cada cliente no tiene pasado: queda a nulo, y eso es correcto.
print([None if pd.isna(v) else round(float(v), 1) for v in df["media_previa"]])
# -> [None, 10.0, 20.0, None, 5.0, 5.0]
