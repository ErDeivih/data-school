import math

contactos = 480_000          # objetos en el destino
cambiados_dia = 3_200        # los que de verdad cambiaron hoy
lote = 200                   # registros por llamada
ritmo = 5                    # llamadas por segundo que permite la API

def sincronizar(filas, lote, ritmo):
    """Devuelve (llamadas, segundos) para escribir esas filas."""
    llamadas = math.ceil(filas / lote)
    return llamadas, llamadas / ritmo

for nombre, filas in (("carga completa", contactos), ("solo cambiados", cambiados_dia)):
    llamadas, segundos = sincronizar(filas, lote, ritmo)
    print(f"{nombre:>15}: {llamadas:5d} llamadas, {segundos:8.1f} s")
# ->  carga completa:  2400 llamadas,    480.0 s
# ->  solo cambiados:    16 llamadas,      3.2 s
print("factor:", contactos // cambiados_dia)   # -> 150
