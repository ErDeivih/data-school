# 10 resultados de un buscador, ya ordenados de mas a menos relevante
# Una lista de Python, no un np.array: aqui solo hace falta recorrerla.
relevancias = [1, 0, 1, 0, 0, 1, 0, 0, 0, 0]

aciertos, suma = 0, 0.0
# enumerate(..., start=1) devuelve (posicion, valor) empezando a contar en 1: asi `posicion`
# es el numero de resultados que llevas vistos, que es el denominador de la precision.
for posicion, rel in enumerate(relevancias, start=1):
    if rel == 1:
        aciertos += 1
        suma += aciertos / posicion     # precision en el punto en que aparece el relevante

total = sum(relevancias)                # cuantos relevantes hay en total
ap = suma / total                       # media de las precisiones en cada relevante
azar = total / len(relevancias)         # la prevalencia: la linea base de la curva PR

print(f"AP          {ap:.4f}")                      # -> 0.7222
print(f"prevalencia {azar:.4f}")                    # -> 0.3000
print(f"veces mejor que el azar {ap / azar:.1f}")   # -> 2.4

# sklearn.metrics.average_precision_score hace esta misma suma escalonada.
