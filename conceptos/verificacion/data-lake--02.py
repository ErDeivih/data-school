# Coste de los ficheros pequenos: no es el espacio, es el numero de aperturas
tam_dia_gb = 4
print("ficheros al dia con micro-lotes de 1 minuto:", 24 * 60)                 # -> ficheros al dia con micro-lotes de 1 minuto: 1440
print("MB por fichero de 1 minuto:", round(tam_dia_gb * 1024 / (24 * 60), 1))  # -> MB por fichero de 1 minuto: 2.8
print("ficheros al ano:", 24 * 60 * 365)                                       # -> ficheros al ano: 525600
print("ficheros al dia compactando por hora:", 24)                             # -> ficheros al dia compactando por hora: 24
print("GB retenidos en 5 anos:", tam_dia_gb * 365 * 5)                         # -> GB retenidos en 5 anos: 7300
