import pandas as pd

# Dos pedidos reales; el orquestador lanza la tarea 3 veces por un timeout.
pedidos = pd.DataFrame({"pedido_id": ["P1", "P2"], "importe": [100, 250]})

# Append puro: cada reintento vuelve a insertar las mismas filas.
append = pd.concat([pedidos] * 3, ignore_index=True)
print(f"append  filas {len(append)}  suma {append['importe'].sum()}")   # -> append  filas 6  suma 1050

# Upsert por clave natural: el destino indexa por pedido_id y sobreescribe.
destino = {}
for _ in range(3):
    for fila in pedidos.itertuples(index=False):
        destino[fila.pedido_id] = fila.importe
print(f"upsert  filas {len(destino)}  suma {sum(destino.values())}")    # -> upsert  filas 2  suma 350
