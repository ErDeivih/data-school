import cProfile
import pstats
from io import StringIO

def transformar(filas):
    return [fila for fila in filas if fila % 3 == 0]   # comprension: se llama una sola vez

def recorrer(filas):
    total = 0
    for fila in filas:              # recorrer una lista grande es lo caro
        total += fila
    return total

def trabajo():
    for _ in range(30):             # 30 llamadas: el perfil contara exactamente eso
        recorrer(range(20_000))     # range no crea la lista de 20.000 numeros
    transformar(list(range(20_000)))   # aqui si: list() materializa los 20.000

perfil = cProfile.Profile()
perfil.enable()          # a partir de aqui, cada llamada queda instrumentada y cronometrada
trabajo()
perfil.disable()

flujo = StringIO()       # print_stats vuelca cientos de lineas: se guardan en memoria, no en pantalla
estadisticas = pstats.Stats(perfil, stream=flujo).sort_stats("tottime")
estadisticas.print_stats()
informe = flujo.getvalue()

# stats guarda una fila por funcion: (fichero, linea, nombre) -> (llamadas, ...)
def llamadas_a(funcion):
    # v[0] es el numero de llamadas: se busca la fila cuyo nombre de funcion coincide.
    return next(v[0] for k, v in estadisticas.stats.items() if k[2] == funcion.__name__)

print("llamadas a recorrer:", llamadas_a(recorrer))            # -> 30
print("llamadas a transformar:", llamadas_a(transformar))      # -> 1
print("lineas del informe:", len(informe.splitlines()))
print("el informe ordena por tiempo propio: recorrer encabeza la lista")
