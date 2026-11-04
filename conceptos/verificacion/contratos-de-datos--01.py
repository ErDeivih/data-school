import pandas as pd

# Contrato v1 de un evento de pedido: lo que el productor promete.
contrato = {
    "pedido_id": {"nulos": False, "unico": True},
    "importe_centimos": {"nulos": False, "min": 0},
    "estado": {"nulos": False, "dominio": {"creado", "pagado", "enviado"}},
}

lote = pd.DataFrame({
    "pedido_id": ["P1", "P2", "P3", "P3"],
    "importe_centimos": [1599, -250, 800, 420],
    "estado": ["pagado", "creado", "devuelto", "enviado"],
})

def validar(df, contrato):
    """Devuelve la lista de incumplimientos; vacia significa que el lote cumple."""
    fallos = []
    for col, regla in contrato.items():
        if col not in df.columns:
            fallos.append(f"falta la columna {col}")
            continue
        if not regla["nulos"] and df[col].isna().any():
            fallos.append(f"{col}: hay nulos")
        if regla.get("unico") and df[col].duplicated().any():
            fallos.append(f"{col}: hay duplicados ({int(df[col].duplicated().sum())})")
        if "min" in regla and (df[col] < regla["min"]).any():
            fallos.append(f"{col}: {int((df[col] < regla['min']).sum())} valores por debajo de {regla['min']}")
        if "dominio" in regla:
            fuera = sorted(set(df[col]) - regla["dominio"])
            if fuera:
                fallos.append(f"{col}: valores fuera del dominio {fuera}")
    return fallos

for fallo in validar(lote, contrato):
    print("FALLO", fallo)
# -> FALLO pedido_id: hay duplicados (1)
# -> FALLO importe_centimos: 1 valores por debajo de 0
# -> FALLO estado: valores fuera del dominio ['devuelto']
