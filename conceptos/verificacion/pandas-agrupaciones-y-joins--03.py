import pandas as pd

g = pd.DataFrame({"ciudad": ["M", "M", "S"], "importe": [10.0, None, 5.0]})
print(g.groupby("ciudad")["importe"].size().to_dict())    # -> {'M': 2, 'S': 1}  (filas)
print(g.groupby("ciudad")["importe"].count().to_dict())   # -> {'M': 1, 'S': 1}  (no nulos)

# Las claves nulas desaparecen del groupby salvo que lo pidas explicitamente
k = pd.DataFrame({"g": ["a", None, "a"], "v": [1.0, 2.0, 3.0]})
print(k.groupby("g")["v"].sum().to_dict())               # -> {'a': 4.0}
print(len(k.groupby("g", dropna=False)["v"].sum()))      # -> 2

piv = pd.DataFrame({"mes": ["ene", "ene", "ene", "feb"],
                    "ciudad": ["M", "M", "S", "M"],
                    "importe": [1.0, 2.0, 4.0, 8.0]})
print(piv.pivot_table(index="mes", columns="ciudad", values="importe", aggfunc="sum").to_numpy().tolist())
# -> [[3.0, 4.0], [8.0, nan]]
print(piv.pivot_table(index="mes", columns="ciudad", values="importe").to_numpy().tolist())
# -> [[1.5, 4.0], [8.0, nan]]  (sin aggfunc, pivot_table usa la media)
