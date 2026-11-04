# Perfil minimo: para cada columna, cuantos huecos hay y cuantos valores distintos.
crudo = {
    "pedido_id": [1, 2, 3, 4, 5, 6],
    "pais":      ["ES", "ES", "ES", "ES", "ES", "ES"],
    "ciudad":    ["Madrid", "Barcelona", "madrid", "Valencia", "Barcelona", " Sevilla"],
    "importe":   [120.5, 80.0, 45.25, None, 999999.0, 60.0],
    "alta":      ["2024-01-05", "2024-01-05", "2024-01-06",
                  "2024-01-07", "1900-01-01", "2024-01-08"],
}
filas = len(next(iter(crudo.values())))

print(f"{'columna':<10}{'nulos':>7}{'distintos':>11}{'cardinalidad':>14}")
for nombre, valores in crudo.items():
    nulos = sum(1 for v in valores if v is None)
    distintos = len({v for v in valores if v is not None})
    print(f"{nombre:<10}{nulos:>7}{distintos:>11}{distintos / filas:>14.2f}")

# La cardinalidad depende de haber normalizado antes: 5 valores son 4 categorias.
normalizadas = {c.strip().lower() for c in crudo["ciudad"]}
print("ciudad distintos sin normalizar", len(set(crudo["ciudad"])),
      " normalizando", len(normalizadas))
# -> ciudad distintos sin normalizar 5  normalizando 4
