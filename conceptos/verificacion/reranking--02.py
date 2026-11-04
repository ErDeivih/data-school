# Tiempo de consulta segun el tamano del conjunto de candidatos. Los numeros por pareja
# son hipotesis de trabajo (0,5 ms en CPU), no una medida publicada: lo que importa es la forma.
candidatos = [50, 100, 200, 500]
ms_por_pareja = 0.5
ms_recuperacion = 25.0        # busqueda en el indice vectorial, constante con m

for m in candidatos:
    # el coste del reordenador es lineal en el numero de candidatos: m ejecuciones del modelo
    reorden = m * ms_por_pareja
    # el total se imprime con formato de anchura fija para que las columnas queden alineadas
    print(f"candidatos {m:>3}  reordenar {reorden:>6.1f} ms  "
          f"total {ms_recuperacion + reorden:>6.1f} ms  "
          f"coste relativo {(ms_recuperacion + reorden) / ms_recuperacion:.1f}x")
