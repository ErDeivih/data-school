import numpy as np

# Serie semanal y sus tres acciones corporativas. Los eventos se declaran con su FACTOR DE
# PRECIO, que es un dato del evento y no del movimiento del día: un split 1:2 parte el precio
# (0,5) y un contrasplit 3:2 lo multiplica por 1,5. Antes esto usaba el salto bruto observado,
# y con eso la serie ajustada daba siempre 0 % en los eventos: se daba por supuesto lo que
# había que medir.
fechas = np.array(["2024-01-05", "2024-02-09", "2024-02-16", "2024-03-15", "2024-03-22",
                   "2024-04-26", "2024-05-03"], dtype="datetime64[D]")
bruto = np.array([100.0, 103.0, 75.0, 69.0, 74.0, 78.0, 117.0])
# (posicion de la fecha ex, dividendo por accion, factor de precio del evento)
eventos = {2: (0.0, 0.5), 4: (1.5, 1.0), 6: (0.0, 1.5)}

# DIVISOR: el indice ajustado es bruto / divisor, y el divisor se ajusta en cada evento para
# que el indice no salte por un cambio de formato del precio.
divisor = np.ones(len(bruto))
d = 1.0
for i in range(len(bruto)):
    if i in eventos:
        d *= eventos[i][1]
    divisor[i] = d

ajustado = bruto / divisor
print(np.round(divisor, 4).tolist())
print(np.round(ajustado, 3).tolist())

# El salto del dia del split: bruto contra ajustado. El bruto se hunde un 27,18 %; el ajustado
# sube un 45,63 %, que es el movimiento real del dia.
print(round(bruto[2] / bruto[1] - 1, 4))
print(round(ajustado[2] / ajustado[1] - 1, 4))
# El salto del dia del split: bruto contra ajustado.
print(round(bruto[2] / bruto[1] - 1, 4))          # -> -0.2718  (el precio parece hundirse)
print(round(indice[2] / indice[1] - 1, 4))        # -> 0.0      (no paso nada)

# El salto del dia del dividendo: el precio SUBE y la rentabilidad del accionista baja.
print(round(bruto[4] / bruto[3] - 1, 4))          # -> 0.0725
print(round((bruto[4] + 1.5) / bruto[3] - 1, 4))  # -> 0.0942  el salto real, (74 + 1,5) / 69

# Rentabilidad del periodo: 100 invertidos el 5 de enero.
print(round(indice[-1] - 100, 4))                 # -> -2.1023 % con el dividendo cobrado
print(round(bruto[-1] / bruto[0] * 100 - 100, 4))  # -> 17.0 % solo con el precio
