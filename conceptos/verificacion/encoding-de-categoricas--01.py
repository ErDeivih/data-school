import pandas as pd

ciudades = pd.DataFrame({"ciudad": ["Madrid", "Lugo", "Madrid", "Sevilla", "Lugo"]})

# Una columna por categoria; con drop_first se quita la referencia y se evita la colinealidad.
todas = pd.get_dummies(ciudades, columns=["ciudad"])
sin_una = pd.get_dummies(ciudades, columns=["ciudad"], drop_first=True)

print(f"columnas sin drop_first {todas.shape[1]}")    # -> 3
print(f"columnas con drop_first {sin_una.shape[1]}")  # -> 2
print("columnas:", list(sin_una.columns))            # -> ['ciudad_Madrid', 'ciudad_Sevilla']
