from itertools import combinations

def subset_sum_verificar(numeros, objetivo, certificado):
    """Verificar es polinomico: basta sumar el candidato y comprobar."""
    return sum(certificado) == objetivo and set(certificado) <= set(numeros)

def subset_sum_buscar(numeros, objetivo):
    """Buscar es exponencial: hay que probar subconjuntos de todos los tamanos."""
    intentos = 0
    for tam in range(len(numeros) + 1):
        for candidato in combinations(numeros, tam):
            intentos += 1
            if sum(candidato) == objetivo:
                return list(candidato), intentos
    return None, intentos

numeros = [3, 34, 4, 12, 5, 2]
solucion, intentos = subset_sum_buscar(numeros, 9)
print("solucion:", solucion)                    # -> solucion: [4, 5]
print("intentos de busqueda:", intentos)        # -> intentos de busqueda: 18
print("verificacion:", subset_sum_verificar(numeros, 9, solucion))   # -> verificacion: True
print("subconjuntos posibles con n=6:", 2 ** 6)  # -> subconjuntos posibles con n=6: 64
