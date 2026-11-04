import pandas as pd

# Target encoding crudo frente a dejar fuera la propia fila.
df = pd.DataFrame({
    "ciudad": ["A", "A", "A", "B", "B", "B"],
    "compro": [1, 0, 1, 0, 0, 1],
})

crudo = df.groupby("ciudad")["compro"].transform("mean")
suma = df.groupby("ciudad")["compro"].transform("sum")
cuenta = df.groupby("ciudad")["compro"].transform("count")
fuera = (suma - df["compro"]) / (cuenta - 1)   # media sin la propia fila

print(f"media global      {df['compro'].mean():.2f}")     # -> 0.50
print("encoding crudo   ", crudo.round(2).tolist())      # -> [0.67, 0.67, 0.67, 0.33, 0.33, 0.33]
print("dejando uno fuera", fuera.round(2).tolist())      # -> [0.5, 1.0, 0.5, 0.5, 0.5, 0.0]
