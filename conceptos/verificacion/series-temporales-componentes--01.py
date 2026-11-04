import numpy as np

# 24 meses construidos a mano: tendencia + estacionalidad anual + ruido que alterna.
meses = np.arange(24)
tendencia = 100 + 2.0 * meses
estacionalidad = 10 * np.sin(2 * np.pi * meses / 12)   # un ciclo completo cada 12 meses
ruido = np.array([1.0, -1.0] * 12)

serie = tendencia + estacionalidad + ruido

print(f"mes 0  {serie[0]:.1f}")    # -> 101.0
print(f"mes 3  {serie[3]:.1f}")    # -> 115.0
print(f"mes 6  {serie[6]:.1f}")    # -> 113.0
print(f"mes 12 {serie[12]:.1f}")   # -> 125.0

# La descomposicion aditiva se deshace restando: la tendencia vuelve exacta.
print(f"tendencia recuperada {np.allclose(serie - estacionalidad - ruido, tendencia)}")  # -> True
