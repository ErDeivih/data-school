import numpy as np

# El coste de equilibrio se calcula ANTES de mirar la estrategia: es una condicion de viabilidad
for giro, bruto_por_giro in ((0.10, 0.0004), (0.25, 0.0004), (0.43, 0.0004), (0.43, 0.00015)):
    equilibrio_pb = 1e4 * bruto_por_giro
    coste_anual = giro * 252 * 0.0005
    print("giro %.2f  bruto por giro %.2f pb  equilibrio %.2f pb  coste anual a 5 pb %.2f%%"
          % (giro, 1e4 * bruto_por_giro, equilibrio_pb, 100 * coste_anual))
# -> giro 0.10  bruto por giro 4.00 pb  equilibrio 4.00 pb  coste anual a 5 pb 1.26%
# -> giro 0.25  bruto por giro 4.00 pb  equilibrio 4.00 pb  coste anual a 5 pb 3.15%
# -> giro 0.43  bruto por giro 4.00 pb  equilibrio 4.00 pb  coste anual a 5 pb 5.42%
# -> giro 0.43  bruto por giro 1.50 pb  equilibrio 1.50 pb  coste anual a 5 pb 5.42%
