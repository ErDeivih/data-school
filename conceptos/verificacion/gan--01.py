import numpy as np

# Discriminador optimo: D*(x) = p_d(x) / (p_d(x) + p_g(x)).
# La senal que llega al generador incluye dD/da = D*(1 - D*).
p_d = np.array([0.001, 0.02, 0.30, 0.50, 0.90])
p_g = np.array([0.90, 0.50, 0.30, 0.02, 0.001])
# La division va elemento a elemento: son dos arrays de la misma forma, no matrices.
D = p_d / (p_d + p_g)

print("zona      D*   minimax D(1-D)   no saturada 1-D")
for i, d in enumerate(D):
    print(f"{i:>4}  {d:6.3f}  {d * (1 - d):14.5f}  {1 - d:14.5f}")
# -> zona      D*   minimax D(1-D)   no saturada 1-D
# ->    0   0.001         0.00111         0.99889
# ->    1   0.038         0.03698         0.96154
# ->    2   0.500         0.25000         0.50000
# ->    3   0.962         0.03698         0.03846
# ->    4   0.999         0.00111         0.00111
