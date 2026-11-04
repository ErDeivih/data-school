def mochila_voraz(pesos, valores, capacidad):
    """Coge primero lo de mayor valor por kilo. Es la regla natural y no siempre es optima."""
    orden = sorted(range(len(pesos)), key=lambda i: valores[i] / pesos[i], reverse=True)
    elegidos, peso, valor = [], 0, 0
    for i in orden:
        if peso + pesos[i] <= capacidad:
            elegidos.append(i); peso += pesos[i]; valor += valores[i]
    return elegidos, valor

def mochila_optima(pesos, valores, capacidad):
    """Fuerza bruta: prueba las 2^n combinaciones. Solo vale para n pequeno."""
    mejor, mejor_valor = (), 0
    for mascara in range(1 << len(pesos)):
        peso = valor = 0
        for i in range(len(pesos)):
            if mascara >> i & 1:
                peso += pesos[i]; valor += valores[i]
        if peso <= capacidad and valor > mejor_valor:
            mejor, mejor_valor = mascara, valor
    return mejor, mejor_valor

pesos, valores, capacidad = [6, 5, 5], [30, 24, 24], 10
print("densidades:", [round(v / p, 2) for p, v in zip(pesos, valores)])  # -> densidades: [5.0, 4.8, 4.8]
print("voraz:  ", mochila_voraz(pesos, valores, capacidad))    # -> voraz:   ([0], 30)
print("optimo: ", mochila_optima(pesos, valores, capacidad))   # -> optimo:  (6, 48)
print("el voraz pierde:", 48 - 30, "de 48")                    # -> el voraz pierde: 18 de 48
