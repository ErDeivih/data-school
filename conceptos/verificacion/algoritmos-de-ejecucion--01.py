# Reparto VWAP sobre un perfil de volumen con forma de U, con limite de participacion
Q = 50_000                          # acciones que hay que comprar
tramos = [430_000, 150_000, 100_000, 150_000, 620_000]   # volumen del mercado por tramo
LIMITE = 0.05                       # nunca mas del 5 % del volumen del tramo

total = sum(tramos)
enviado = []
for i, volumen in enumerate(tramos, start=1):
    rodaja = Q * volumen / total    # peso proporcional al volumen: la definicion de VWAP
    tope = LIMITE * volumen
    real = min(rodaja, tope)
    enviado.append(real)
    print(f"tramo {i}: pediria {rodaja:>7.0f}, tope {tope:>7.0f}, manda {real:>7.0f} "
          f"({real / volumen:.2%} del volumen)")
# -> tramo 1: pediria   14828, tope   21500, manda   14828 (3.45% del volumen)
# -> tramo 2: pediria    5172, tope    7500, manda    5172 (3.45% del volumen)
# -> tramo 3: pediria    3448, tope    5000, manda    3448 (3.45% del volumen)
# -> tramo 4: pediria    5172, tope    7500, manda    5172 (3.45% del volumen)
# -> tramo 5: pediria   21379, tope   31000, manda   21379 (3.45% del volumen)
print(f"total enviado: {sum(enviado):.0f} de {Q}  (falta {Q - sum(enviado):.0f})")
# -> total enviado: 50000 de 50000  (falta 0)
