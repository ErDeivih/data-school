import numpy as np

# Serie mensual de dos tiendas y del total, para la que solo tenemos el pronostico,
# no el dato real. Lo que se comprueba aqui es la aritmetica de la reconciliacion.
base = np.array([1200.0, 720.0, 520.0])          # [total, tienda A, tienda B]
S = np.array([[1.0, 1.0],                        # el total es A + B
              [1.0, 0.0],
              [0.0, 1.0]])

print(f"suma de las tiendas {base[1] + base[2]:.1f}   total declarado {base[0]:.1f}")  # -> 1240.0 y 1200.0

# Reconciliacion proporcional: reparte el total segun el peso de cada tienda en la base
peso = base[1:] / base[1:].sum()
reconciliado = S @ (peso * base[0])
print(f"pesos {np.round(peso, 4)}")               # -> [0.5806 0.4194]
print(f"reconciliado {np.round(reconciliado, 1)}")  # -> [1200.  696.8 503.2]
print(f"desajuste tras cuadrar {base[1] + base[2] - base[0]:.1f} -> pendiente")  # -> 40.0
print(f"suma final {reconciliado[1] + reconciliado[2]:.1f}")  # -> 1200.0
