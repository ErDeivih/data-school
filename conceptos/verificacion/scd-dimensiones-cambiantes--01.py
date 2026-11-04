import pandas as pd

CORTE = pd.Timestamp("2025-01-01")     # fecha del cambio que llega del sistema origen
FIN = pd.Timestamp("9999-12-31")       # centinela: version abierta

# Dimension tipo 2: una fila por version, sk unica por fila y nk repetida
dim = pd.DataFrame({
    "sk": [9001, 9002, 9003],
    "nk": [4471, 4471, 8890],
    "ciudad": ["Madrid", "Barcelona", "Sevilla"],
    "inicio": pd.to_datetime(["2019-01-01", "2022-03-15", "2021-06-01"]),
    "fin": pd.to_datetime(["2022-03-15", "9999-12-31", "9999-12-31"]),
    "actual": [False, True, True],
})
origen = pd.DataFrame({"nk": [4471, 8890], "ciudad": ["Valencia", "Sevilla"]})

nuevas, cierres = [], []
for _, o in origen.iterrows():
    vigente = dim[(dim.nk == o.nk) & dim.actual].iloc[0]
    if vigente.ciudad == o.ciudad:      # sin cambio real: no se abre version nueva
        continue
    cierres.append(vigente.sk)
    nuevas.append({"sk": 9000 + len(dim) + len(nuevas) + 1, "nk": o.nk,
                   "ciudad": o.ciudad, "inicio": CORTE, "fin": FIN, "actual": True})

for sk in cierres:                      # la version sustituida se cierra, no se borra
    dim.loc[dim.sk == sk, "fin"] = CORTE
    dim.loc[dim.sk == sk, "actual"] = False
dim = pd.concat([dim, pd.DataFrame(nuevas)], ignore_index=True)

print("filas totales:", len(dim))                                     # -> filas totales: 4
print("versiones del cliente 4471:", int((dim.nk == 4471).sum()))     # -> versiones del cliente 4471: 3
print("ciudad vigente hoy:", dim.loc[(dim.nk == 4471) & dim.actual, "ciudad"].item())  # -> ciudad vigente hoy: Valencia
print("fin de la version 9002:", str(dim.loc[dim.sk == 9002, "fin"].item().date()))    # -> fin de la version 9002: 2025-01-01
