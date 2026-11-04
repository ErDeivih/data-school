import itertools

pesos = [6, 5, 5]
valores = [9, 5, 5]
capacidad = 10

# Optimo entero por fuerza bruta: solo factible porque hay 3 objetos.
mejor = 0
for r in range(len(pesos) + 1):
    for combo in itertools.combinations(range(len(pesos)), r):
        if sum(pesos[i] for i in combo) <= capacidad:
            mejor = max(mejor, sum(valores[i] for i in combo))

# Relajacion lineal de la mochila: se ordena por valor/peso y se parte el ultimo objeto.
orden = sorted(range(len(pesos)), key=lambda i: valores[i] / pesos[i], reverse=True)
restante, cota = capacidad, 0.0
for i in orden:
    if pesos[i] <= restante:
        restante -= pesos[i]
        cota += valores[i]
    else:
        cota += valores[i] * restante / pesos[i]   # fraccion del objeto que cabe
        break

print("optimo entero:", mejor)                          # -> 10
print("relajacion lineal:", round(cota, 2))             # -> 13.0
print("gap de integralidad:", round(cota / mejor, 2))   # -> 1.3
