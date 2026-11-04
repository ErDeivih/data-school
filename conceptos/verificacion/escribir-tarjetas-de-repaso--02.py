# Programador SM-2 simplificado, el mismo que usa el portal. Compara una tarjeta que se
# acierta siempre con una que alterna acierto y fallo: los mismos 8 repasos, otro resultado.
def redondear(v):
    return int(v + 0.5)

def programar(secuencia, ef=2.5):
    reps, intervalo, salida = 0, 0, []
    for acierto in secuencia:
        calidad = 4 if acierto else 1
        if calidad < 3:
            reps, intervalo = 0, 1                 # fallo: la tarjeta vuelve a 1 dia
        else:
            reps += 1
            intervalo = 1 if reps == 1 else 6 if reps == 2 else redondear(intervalo * ef)
        ef = max(1.3, ef + (0.1 - (5 - calidad) * (0.08 + (5 - calidad) * 0.02)))
        salida.append(intervalo)
    return salida

buena = [True] * 8
atascada = [True, False] * 4                       # se falla una de cada dos

print("tarjeta buena   :", programar(buena))
print("dias cubiertos  :", sum(programar(buena)), "con", len(buena), "repasos")
print("tarjeta atascada:", programar(atascada))
print("dias cubiertos  :", sum(programar(atascada)), "con", len(atascada), "repasos")
