import numpy as np

# f(x) = (3x + 1)**4. La regla de la cadena dice f'(x) = 12*(3x+1)**3.
def f(x):
    return (3 * x + 1) ** 4

def df_analitica(x):
    return 12 * (3 * x + 1) ** 3

def df_numerica(x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)   # diferencia central: error O(h^2)

x = 2.0
print("analitica ", round(df_analitica(x), 4))    # salida: 4116.0
print("numerica  ", round(df_numerica(x), 4))     # salida: 4116.0

