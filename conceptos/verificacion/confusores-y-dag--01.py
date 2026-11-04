import pandas as pd

# Formacion (T), salario (Y) y edad (Z). Z influye en las dos: es un confusor.
filas = [
    ("joven", "con", 24000, 200),
    ("joven", "sin", 21000, 100),
    ("mayor", "con", 36000, 100),
    ("mayor", "sin", 33000, 300),
]
df = pd.DataFrame(filas, columns=["edad", "formacion", "salario", "n"])

def media(d):
    return (d["salario"] * d["n"]).sum() / d["n"].sum()

bruto = media(df[df.formacion == "con"]) - media(df[df.formacion == "sin"])
print(f"diferencia bruta {bruto:+,.0f}")             # -> diferencia bruta -2,000

# Fórmula de ajuste: efecto dentro de cada estrato, ponderado por su tamaño.
estratos = []
for edad, grupo in df.groupby("edad"):
    dif = media(grupo[grupo.formacion == "con"]) - media(grupo[grupo.formacion == "sin"])
    estratos.append((dif, grupo["n"].sum()))

pesos = sum(n for _, n in estratos)
print(f"diferencia ajustada {sum(d * n for d, n in estratos) / pesos:+,.0f}")
# -> diferencia ajustada +3,000
