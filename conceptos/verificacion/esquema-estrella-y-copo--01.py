# Estrella (1 union) y copo (3 uniones): mismo resultado, distinto numero de saltos
DIM_ESTRELLA = {1: ("teclado", "perifericos", "accesorios"),
                2: ("raton", "perifericos", "accesorios"),
                3: ("monitor", "pantallas", "imagen")}

DIM_PRODUCTO = {1: ("teclado", 10), 2: ("raton", 10), 3: ("monitor", 20)}
DIM_FAMILIA = {10: ("perifericos", 100), 20: ("pantallas", 200)}
DIM_DEPARTAMENTO = {100: "accesorios", 200: "imagen"}

VENTAS = [(1, 59.90), (2, 12.50), (3, 179.00)]

estrella, copo = {}, {}
for producto, importe in VENTAS:
    departamento = DIM_ESTRELLA[producto][2]                        # 1 salto
    copo_dep = DIM_DEPARTAMENTO[DIM_FAMILIA[DIM_PRODUCTO[producto][1]][1]]   # 3 saltos
    estrella[departamento] = round(estrella.get(departamento, 0) + importe, 2)
    copo[copo_dep] = round(copo.get(copo_dep, 0) + importe, 2)

print("estrella (1 union)  :", estrella)     # -> {'accesorios': 72.4, 'imagen': 179.0}
print("copo     (3 uniones):", copo)         # -> {'accesorios': 72.4, 'imagen': 179.0}
print("mismo resultado     :", estrella == copo)   # -> True
