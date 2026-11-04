# Cuanto cuesta registrar: cada linea se escribe, se transporta, se indexa y se guarda.
rps, bytes_por_linea = 200, 250

def por_dia(lineas_por_peticion):
    # 86400 son los segundos del dia: la formula entera cabe en una linea.
    return rps * lineas_por_peticion * bytes_por_linea * 86400

info = por_dia(3)
debug = por_dia(40)

print(f"con INFO  {info / 1e9:6.1f} GB al dia")     # ->   13.0 GB al dia
print(f"con DEBUG {debug / 1e9:6.1f} GB al dia")    # ->  172.8 GB al dia
print(f"multiplicador {debug / info:.0f} x")        # -> 13 x
print(f"un mes en DEBUG: {debug * 30 / 1e12:.1f} TB")  # -> 5.2 TB
