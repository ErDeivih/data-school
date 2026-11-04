import csv
import io

# Leer un CSV con el separador equivocado: no falla, devuelve una sola columna de texto
crudo = "producto;importe\nteclado;29,95\nraton;12,50\n"

mal = list(csv.reader(io.StringIO(crudo)))
print("columnas mal :", mal[0], "filas", len(mal) - 1)          # -> ['producto;importe'] filas 2
print("tipo mal     :", type(mal[1][1]).__name__, "en vez de float")   # -> str en vez de float

bien = list(csv.reader(io.StringIO(crudo), delimiter=";"))
print("columnas bien:", bien[0])                                 # -> ['producto', 'importe']
importe = [float(f[1].replace(",", ".")) for f in bien[1:]]
print("media        :", round(sum(importe) / len(importe), 3))   # -> 21.225
