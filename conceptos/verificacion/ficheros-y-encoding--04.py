import csv
import io

# Un campo con el separador y comillas dentro: CSV lo resuelve doblando las comillas
linea = 'producto;importe;nota\n"teclado; inalambrico";29,95;"dice ""oferta"" y ; sigue"\n'
filas = list(csv.reader(io.StringIO(linea), delimiter=";"))

print("columnas por fila:", [len(f) for f in filas])   # -> [3, 3]
print("campo con ';'    :", filas[1][0])               # -> teclado; inalambrico
print("comillas dobladas:", filas[1][2])               # -> dice "oferta" y ; sigue
