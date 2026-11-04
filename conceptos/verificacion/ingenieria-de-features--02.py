import pandas as pd

# Ninguna columna separa las clases por si sola; el cociente si.
df = pd.DataFrame({
    "visitas": [10, 20, 30, 40, 12, 24, 36, 48],
    "compras": [2, 4, 6, 8, 6, 12, 18, 24],
    "convierte": [0, 0, 0, 0, 1, 1, 1, 1],
})
df["tasa"] = df["compras"] / df["visitas"]
g = df.groupby("convierte")[["visitas", "tasa"]].mean()

print(f"visitas medias clase 0 {g.loc[0, 'visitas']:.1f}  clase 1 {g.loc[1, 'visitas']:.1f}")
# -> visitas medias clase 0 25.0  clase 1 30.0
print(f"tasa media     clase 0 {g.loc[0, 'tasa']:.2f}  clase 1 {g.loc[1, 'tasa']:.2f}")
# -> tasa media     clase 0 0.20  clase 1 0.50
