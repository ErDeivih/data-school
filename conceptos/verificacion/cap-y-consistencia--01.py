# W + R > N hace que el conjunto que escribe y el que lee se crucen en algun nodo.
for n in (3, 5):
    # Lista por comprension con dos for anidados: recorre todas las parejas (w, r) y se queda
    # con las que cumplen la condicion. Se lee como "para cada w, para cada r, si w+r>n".
    validas = [(w, r) for w in range(1, n + 1) for r in range(1, n + 1) if w + r > n]
    print(f"N={n}: {len(validas)} combinaciones validas de {n * n}")
    # join con generador: une los textos con un espacio en vez de imprimir la lista con corchetes.
    print("  ", " ".join(f"W{w}R{r}" for w, r in validas))
    # key=lambda x: x[0] + x[1] ordena las parejas por su suma, no por el primer elemento.
    minimo = min(validas, key=lambda x: x[0] + x[1])
    print("   suma minima:", f"W{minimo[0]}R{minimo[1]}", "=", minimo[0] + minimo[1])
