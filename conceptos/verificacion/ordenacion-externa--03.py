# Cuanto trafico de disco cuesta ordenar segun las vias de la fusion.
def movidos(n, M, k, bytes_registro=100):
    """Registros movidos entre memoria y disco, y numero de rondas de fusion."""
    vueltas, rondas = -(-n // M), 0            # -(-a // b) es la division hacia arriba
    while vueltas > 1:
        vueltas = -(-vueltas // k)             # cada ronda junta k vueltas en una
        rondas += 1
    return 2 * n * (1 + rondas), rondas        # 2n al crear vueltas + 2n por ronda

n, M = 100_000_000, 1_000_000                  # 10 GB de registros de 100 bytes, 100 MB de memoria
print("vueltas de la fase 1:", -(-n // M))     # -> vueltas de la fase 1: 100
for k in (4, 10, 100):
    registros, rondas = movidos(n, M, k)
    print(f"k={k:3d}  rondas={rondas}  trafico={registros * 100 / 1e9:5.0f} GB")
# -> k=  4  rondas=4  trafico=  100 GB
# -> k= 10  rondas=2  trafico=   60 GB
# -> k=100  rondas=1  trafico=   40 GB
