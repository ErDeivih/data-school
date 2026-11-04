import numpy as np

capital = np.array([10000, 10500, 11200, 10800, 10100, 9500,
                    10200, 11000, 11600, 11400, 12100, 12400], dtype=float)
meses = np.arange(1, capital.size + 1)

picos = np.maximum.accumulate(capital)      # maximo alcanzado hasta cada mes
caidas = (picos - capital) / picos          # drawdown en cada mes
i_fondo = int(caidas.argmax())
i_pico = int(capital[:i_fondo + 1].argmax())
vuelta = np.flatnonzero(capital[i_fondo:] >= capital[i_pico])

print(f"pico         mes {meses[i_pico]:>2}  {capital[i_pico]:>7.0f}")   # -> mes  3    11200
print(f"fondo        mes {meses[i_fondo]:>2}  {capital[i_fondo]:>7.0f}")  # -> mes  6     9500
print(f"caida maxima {caidas[i_fondo]:.2%}")                              # -> 15.18%
print(f"duracion     {meses[i_fondo + vuelta[0]] - meses[i_pico]} meses")  # -> 6 meses
print(f"recuperacion {(capital[i_pico] / capital[i_fondo] - 1):.2%}")      # -> 17.89%
