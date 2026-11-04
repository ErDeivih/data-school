# La ficha del conjunto de datos: lo primero que va en el README del proyecto.
import pandas as pd

df = pd.DataFrame({
    "distrito": ["Centro", "Centro", "Norte", "Norte", "Sur", "Sur", "Este", "Oeste"],
    "precio_m2": [14.2, 13.8, 9.1, None, 7.4, 8.0, 10.5, 11.2],
})
# El resumen que cualquiera tiene que poder ver sin abrir el notebook.
print(f"filas {len(df)}")
print(f"nulos en precio_m2 {int(df['precio_m2'].isna().sum())} de {len(df)}")
print(f"distritos {df['distrito'].nunique()}, mediana {df['precio_m2'].median():.1f} EUR/m2")
