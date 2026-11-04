import numpy as np

# Selectividad = valores distintos / filas. Un indice sobre una columna con dos
# valores no ahorra lecturas: la consulta devuelve media tabla de todas formas.
rng = np.random.default_rng(0)
activo = rng.integers(0, 2, size=100_000)          # columna booleana
factura = rng.integers(1, 100_001, size=100_000)   # identificador de factura

print(f"activo   distintos {np.unique(activo).size:>6}  selectividad {np.unique(activo).size / activo.size:.7f}")
# -> activo   distintos      2  selectividad 0.0000200
print(f"factura  distintos {np.unique(factura).size:>6}  selectividad {np.unique(factura).size / factura.size:.1f}")
# -> factura  distintos  63232  selectividad 0.6
