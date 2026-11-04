import pandas as pd

largo = pd.DataFrame({
    "cliente": ["A", "A", "A", "B", "B"],
    "mes": ["ene", "feb", "mar", "ene", "mar"],
    "ventas": [1, 2, 3, 4, 6],
})
ancho = largo.pivot(index="cliente", columns="mes", values="ventas")

print(ancho.shape)                          # -> (2, 3)
print(ancho.loc["B"].tolist())              # -> [4.0, nan, 6.0]  falta B-feb
print(int(ancho.isna().sum().sum()), ancho.size)   # -> 1 6

# pivot NO agrega: con un par (cliente, mes) repetido lanza un error en vez de sumar
repetido = pd.concat([largo, largo.iloc[[0]]])
try:
    repetido.pivot(index="cliente", columns="mes", values="ventas")
except ValueError as e:
    print(str(e))                           # -> Index contains duplicate entries, cannot reshape

# pivot_table es la que agrega; aqui se le dice explicitamente que sume
print(repetido.pivot_table(index="cliente", columns="mes", values="ventas",
                           aggfunc="sum").loc["A"].tolist())   # -> [2.0, 2.0, 3.0]
