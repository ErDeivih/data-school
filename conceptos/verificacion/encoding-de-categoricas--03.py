import pandas as pd

# Categoria frecuente (100 filas) y categoria rara (4 filas).
df = pd.DataFrame({"cat": ["A"] * 100 + ["B"] * 4,
                   "y": [1] * 60 + [0] * 40 + [1, 1, 1, 0]})

prior = df["y"].mean()
g = df.groupby("cat")["y"].agg(["count", "mean"])
m = 10   # fuerza del suavizado: cuantas filas virtuales del prior se anaden

# El suavizado arrastra la categoria con pocos datos hacia la media global.
suave = (g["count"] * g["mean"] + m * prior) / (g["count"] + m)

print(f"media global (prior)  {prior:.2f}")                  # -> 0.61
print("medias crudas       ", g["mean"].round(2).to_dict())  # -> {'A': 0.6, 'B': 0.75}
print("medias suavizadas   ", suave.round(2).to_dict())      # -> {'A': 0.6, 'B': 0.65}
