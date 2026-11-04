import pandas as pd

# Eventos a predecir: compra (1) o no compra (0) de un cliente.
eventos = pd.DataFrame({
    "cliente": [1, 1],
    "t_evento": pd.to_datetime(["2024-03-10", "2024-03-25"]),
    "objetivo": [1, 0],
})

# Historial de la variable, con el instante en que cada valor era el vigente.
snapshots = pd.DataFrame({
    "cliente": [1, 1, 1],
    "t_valor": pd.to_datetime(["2024-03-01", "2024-03-10", "2024-03-20"]),
    "saldo_30d": [700.0, 850.0, 900.0],
})

# Union as-of: para cada evento, el ultimo valor conocido en o antes de su fecha.
pit = pd.merge_asof(eventos.sort_values("t_evento"), snapshots.sort_values("t_valor"),
                    left_on="t_evento", right_on="t_valor", by="cliente",
                    direction="backward")
print("point-in-time", pit["saldo_30d"].tolist())     # -> point-in-time [850.0, 900.0]

# Lo que hace una union normal: coge el valor mas reciente para TODOS los eventos.
naive = eventos.merge(snapshots.sort_values("t_valor").groupby("cliente").tail(1), on="cliente")
print("union ingenua ", naive["saldo_30d"].tolist())  # -> union ingenua  [900.0, 900.0]
