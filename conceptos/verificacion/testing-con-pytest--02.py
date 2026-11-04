# Probar el camino de error: la parte que casi nadie escribe.
import pandas as pd

def limpia_pedidos(df: pd.DataFrame) -> pd.DataFrame:
    if (df["centimos"] < 0).any():
        raise ValueError("hay importes negativos en el lote")
    return df.dropna(subset=["fecha"]).copy()

malo = pd.DataFrame({"id": [1], "centimos": [-100], "fecha": ["2024-01-05"]})

try:
    limpia_pedidos(malo)
    print("ERROR: deberia haber lanzado ValueError")
except ValueError as exc:
    print("lanza ValueError:", str(exc))
