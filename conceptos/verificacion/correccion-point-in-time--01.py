import pandas as pd

filas = [
    {"cuenta": "A", "cierre": "2025-03-31", "publicado": "2025-04-24", "ingresos": 100.0},
    {"cuenta": "A", "cierre": "2025-03-31", "publicado": "2025-06-12", "ingresos": 103.0},
    {"cuenta": "B", "cierre": "2025-03-31", "publicado": "2025-04-28", "ingresos": 50.0},
]
df = pd.DataFrame(filas)

def vigente(cuenta, fecha):
    v = df[(df["cuenta"] == cuenta) & (df["publicado"] <= fecha)]
    if v.empty:
        return float("nan")
    return float(v.sort_values("publicado").iloc[-1]["ingresos"])

print(f"A el 2025-05-15 {vigente('A', '2025-05-15'):.1f}")   # -> A el 2025-05-15 100.0
print(f"A el 2025-07-15 {vigente('A', '2025-07-15'):.1f}")   # -> A el 2025-07-15 103.0
print(f"B el 2025-04-10 {vigente('B', '2025-04-10')}")        # -> B el 2025-04-10 nan
print(f"B el 2025-05-15 {vigente('B', '2025-05-15'):.1f}")   # -> B el 2025-05-15 50.0