# La misma idea que un test de pytest, con asserts que se ejecutan de verdad aqui.
import pandas as pd

def limpia_pedidos(df: pd.DataFrame) -> pd.DataFrame:
    """Quita pedidos sin fecha, rechaza importes negativos y pasa centimos a euros."""
    if (df["centimos"] < 0).any():
        raise ValueError("hay importes negativos en el lote")
    limpio = df.dropna(subset=["fecha"]).copy()
    limpio["euros"] = limpio["centimos"] / 100
    return limpio[["id", "euros"]]

entrada = pd.DataFrame({
    "id": [1, 2, 3],
    "centimos": [1050, 999, 0],
    "fecha": ["2024-01-05", None, "2024-01-06"],
})

salida = limpia_pedidos(entrada)

assert len(salida) == 2                      # el pedido sin fecha se cae
assert salida["euros"].iloc[0] == 10.5       # 1050 centimos son 10.5 euros exactos
assert salida["euros"].iloc[1] == 0.0        # un pedido de cero euros no es un nulo
assert list(salida["id"]) == [1, 3]

print("filas de entrada:", len(entrada))
print("filas de salida :", len(salida))
print("euros:", salida["euros"].tolist())
