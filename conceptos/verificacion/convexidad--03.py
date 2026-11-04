import numpy as np

# El hessiano decide: definido positivo -> convexa -> el punto crítico es mínimo global.
H = np.array([[2.0, 4.0], [4.0, 10.0]])
autovalores = np.linalg.eigvalsh(H)

q = lambda v: v[0] ** 2 + 4 * v[0] * v[1] + 5 * v[1] ** 2

print("autovalores del hessiano:", np.round(autovalores, 4))            # salida: [ 0.3431 11.6569]
print("todos positivos        :", bool(np.all(autovalores > 0)))        # salida: True
print("q en el punto critico  :", round(float(q([0.0, 0.0])), 8))       # salida: 0.0

# No es solo el origen: cualquier punto tiene un valor mayor (es el mínimo global)
print("q en (1, -1)           :", round(float(q([1.0, -1.0])), 4))       # salida: 2.0
print("q en (-2, 1)           :", round(float(q([-2.0, 1.0])), 4))       # salida: 1.0
