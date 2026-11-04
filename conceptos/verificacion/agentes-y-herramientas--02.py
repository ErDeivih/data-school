# Divergencia sin limite de pasos: la misma politica repetida se corta con presupuesto.
def bucle_sin_limite(politica):
    # este juguete no ejecuta la politica: solo cuenta hasta su propio tope de 1000
    pasos = 0
    for _ in range(1000):                 # el tope del juguete, no del agente real
        pasos += 1
    return pasos

# repetir la lista 250 veces es lo que hace un agente que no sabe parar
politica_repetida = [("sumar", {"a": 1, "b": 1})] * 250
print("sin presupuesto, un bucle ciego daria", bucle_sin_limite(politica_repetida), "pasos")

for presupuesto in (5, 20, 100):
    # min() evita prometer mas pasos de los que la politica tiene
    ejecutados = min(presupuesto, len(politica_repetida))
    print(f"presupuesto {presupuesto:>3} -> {ejecutados:>3} llamadas y se detiene")
