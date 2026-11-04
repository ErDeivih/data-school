# Cuanto pesa de mas el CSV frente al Parquet: el motivo de no versionar datos.
import io
import pandas as pd

filas = 5000
df = pd.DataFrame({
    "id": range(filas),
    "fecha": pd.date_range("2024-01-01", periods=filas, freq="h"),
    "cliente": [f"C{i % 500:03d}" for i in range(filas)],
    "importe": [round(10 + (i % 97) * 1.5, 2) for i in range(filas)],
})

csv_bytes = df.to_csv(index=False).encode("utf-8")
buffer = io.BytesIO()
df.to_parquet(buffer, compression="zstd")
parquet_bytes = buffer.getvalue()

print("filas:", len(df))
print("CSV     :", len(csv_bytes), "bytes")
print("Parquet :", len(parquet_bytes), "bytes")
print("factor  :", round(len(csv_bytes) / len(parquet_bytes), 1))
