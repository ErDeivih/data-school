import pandas as pd

CIUDADES = ["Barcelona", "Madrid", "Sevilla", "Bilbao"]   # 9, 6, 7 y 6 caracteres
ciudad = pd.Series([CIUDADES[i % 4] for i in range(50_000)])

bytes_normalizado = int(ciudad.str.len().sum())            # ciudad solo en la ficha del cliente
bytes_copiado = bytes_normalizado * 10                     # 10 pedidos por cliente, en promedio
print("bytes de ciudad normalizado:", bytes_normalizado)        # -> bytes de ciudad normalizado: 350000
print("bytes de ciudad copiado:", bytes_copiado)                # -> bytes de ciudad copiado: 3500000
print("factor de duplicacion:", bytes_copiado // bytes_normalizado)  # -> factor de duplicacion: 10

mudanzas = 5_000        # el 10 % de los clientes cambia de ciudad en un ano
print("filas escritas al ano normalizado:", mudanzas)           # -> filas escritas al ano normalizado: 5000
print("filas escritas al ano copiado:", mudanzas * 10)          # -> filas escritas al ano copiado: 50000
