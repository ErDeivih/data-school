# El portal programa el repaso con un SM-2 simplificado. Esto lo reproduce tal cual:
# acierto -> 1 dia, 6 dias y luego intervalo x facilidad; fallo -> vuelve a 1 dia y
# penaliza la facilidad, que nunca baja de 1,3.
def redondear(v):            # redondeo a la mitad hacia arriba, como Math.round en JS
    return int(v + 0.5)

def programar(secuencia, ef=2.5):
    reps, intervalo, salida = 0, 0, []
    for acierto in secuencia:
        calidad = 4 if acierto else 1
        if calidad < 3:
            reps, intervalo = 0, 1                  # fallo: la tarjeta vuelve a 1 dia
        else:
            reps += 1
            intervalo = 1 if reps == 1 else 6 if reps == 2 else redondear(intervalo * ef)
        # La facilidad se actualiza despues de calcular el intervalo, igual que en el portal.
        ef = max(1.3, ef + (0.1 - (5 - calidad) * (0.08 + (5 - calidad) * 0.02)))
        salida.append(intervalo)
    return salida

cinco_aciertos = [True, True, True, True, True]
con_fallo = [True, True, True, False, True, True]

print("cinco aciertos:", programar(cinco_aciertos))   # -> [1, 6, 15, 38, 95]
print("con un fallo  :", programar(con_fallo))        # -> [1, 6, 15, 1, 1, 6]
print("dias cubiertos:", sum(programar(cinco_aciertos)), "con solo 5 repasos")
