# Metodo del potencial: Phi = 2*tamano - capacidad. Si el coste asignado
# (copias + insercion + cambio de Phi) no pasa de 3, el total es 3n como mucho.
def coste_amortizado(n):
    capacidad, tam, total, peor = 0, 0, 0, 0
    for _ in range(n):
        phi_antes = 2 * tam - capacidad
        if tam == capacidad:                  # ampliacion: se copia lo que habia
            copias = tam
            capacidad = capacidad * 2 if capacidad else 1
        else:
            copias = 0
        tam += 1
        phi_despues = 2 * tam - capacidad
        asignado = copias + 1 + phi_despues - phi_antes   # +1 por la propia insercion
        total += asignado
        peor = max(peor, asignado)
    return peor, total

print("peor coste amortizado con n=1024:", coste_amortizado(1024)[0])      # -> 3
print("suma de costes con n=1024:", coste_amortizado(1024)[1])             # -> 3071
print("suma de costes con n=100000:", coste_amortizado(100000)[1])         # -> 299999
