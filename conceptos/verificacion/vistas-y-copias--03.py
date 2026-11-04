import pandas as pd

df = pd.DataFrame({"importe": [10.0, 20.0, 30.0]})
sub = df[df["importe"] > 10]     # subconjunto: comparte bloques hasta que se escribe
sub.iloc[0, 0] = 999.0           # copia al escribir: el padre no cambia
print(df["importe"].tolist())    # -> [10.0, 20.0, 30.0]

# La forma segura y explicita de escribir en la tabla original
df.loc[df["importe"] > 10, "importe"] = 99.0
print(df["importe"].tolist())    # -> [10.0, 99.0, 99.0]
