# La aritmetica de la piramide: donde se va el tiempo de una suite.
# Las dos claves coinciden: un nombre que falte aqui da KeyError al calcular los segundos.
duraciones = {"unitaria": 0.002, "integracion": 0.400, "e2e": 12.0}
cantidades = {"unitaria": 800, "integracion": 120, "e2e": 8}

total = 0.0
# items() da pares (clave, valor): se recorren las dos tablas a la vez sin usar indices.
for capa, n in cantidades.items():
    segundos = n * duraciones[capa]
    total += segundos
    # El formato va en la f-string: <12 alinea a la izquierda, >4 a la derecha, .1f un decimal.
    print(f"{capa:<12} {n:>4} pruebas {segundos:>8.1f} s")

total_pruebas = sum(cantidades.values())       # sum sobre los valores, no sobre las claves
tiempo_e2e = cantidades["e2e"] * duraciones["e2e"]
print(f"total de la suite: {total:.1f} s")                            # -> total de la suite: 145.6 s
# .3% multiplica por 100 y anade el signo: 0.00862 se imprime como 0.862%.
print(f"e2e: {cantidades['e2e'] / total_pruebas:.3%} de las pruebas")  # -> e2e: 0.862% de las pruebas
print(f"e2e: {tiempo_e2e / total:.0%} del tiempo")                     # -> e2e: 66% del tiempo
