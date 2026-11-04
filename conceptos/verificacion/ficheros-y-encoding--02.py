import csv
import io

# Por que un formato columnar ocupa menos: el texto repetido se guarda como codigos
nombres = ["Sanchez", "Nunez", "Gomez", "Ruiz"]
filas = [(f"{i:04d}", nombres[i % 4]) for i in range(2000)]

csv_buf = io.StringIO()
escritor = csv.writer(csv_buf, lineterminator="\n")
escritor.writerow(["pedido_id", "nombre"])
escritor.writerows(filas)
bytes_csv = len(csv_buf.getvalue().encode())

# Modelo de lo que hace un diccionario: cada texto una vez y una clave por fila
diccionario = {n: i for i, n in enumerate(nombres)}
bytes_codigos = sum(len(p) + 2 for p, _ in filas) + sum(len(n) + 1 for n in nombres)

print("csv                    :", bytes_csv, "bytes")             # -> 22517 bytes
print("misma tabla como codigos:", bytes_codigos, "bytes")        # -> 12025 bytes
print("factor                 :", round(bytes_csv / bytes_codigos, 1))   # -> 1.9
print("codigos de la columna nombre:", [diccionario[n] for _, n in filas[:4]])   # -> [0, 1, 2, 3]
