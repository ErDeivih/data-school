import pandas as pd

# Seleccion por grupo: cuantos candidatos pasan el filtro de cada 100.
seleccion = pd.DataFrame({
    "grupo":         ["A", "B"],
    "candidatos":    [1000, 400],
    "seleccionados": [420, 120],
})
seleccion["tasa"] = seleccion.seleccionados / seleccion.candidatos   # division fila a fila

mejor = seleccion.tasa.max()
seleccion["impacto"] = seleccion.tasa / mejor          # regla del 80 %: el mejor grupo es la referencia

print(seleccion.to_string(index=False))                # quita la columna del indice, que aqui no aporta
print("impacto dispar minimo:", f"{seleccion.impacto.min():.2f}")   # .2f redondea solo lo que se imprime
print("regla del 80 %:", "se cumple" if seleccion.impacto.min() >= 0.8 else "NO se cumple")
print("personas de diferencia:", int(seleccion.candidatos[0] * (seleccion.tasa[0] - seleccion.tasa[1])))
