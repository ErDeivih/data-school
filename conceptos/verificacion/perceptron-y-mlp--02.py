import numpy as np

# Una neurona es una recta: el sesgo la desplaza y el peso la gira
x = np.array([-6.0, -2.0, 0.0, 2.0, 6.0])
# np.exp se aplica al array entero: no hace falta recorrerlo con un bucle
sigmoide = 1.0 / (1.0 + np.exp(-x))
print("entradas ", x)                              # -> [-6. -2.  0.  2.  6.]
# np.round devuelve un array nuevo; `sigmoide` sigue con todos sus decimales
print("sigmoide ", np.round(sigmoide, 4))          # -> [0.0025 0.1192 0.5    0.8808 0.9975]

# El mismo peso con signo contrario niega la decision
print("w=-1, b=0:", np.round(1.0 / (1.0 + np.exp(-(-1.0 * x + 0.0))), 4))
# -> [0.9975 0.8808 0.5    0.1192 0.0025]

# Y el sesgo mueve la frontera: con w=1 y b=-2 el corte pasa por x=2
print("w=1, b=-2 :", np.round(1.0 / (1.0 + np.exp(-(1.0 * x - 2.0))), 4))
# -> [0.0003 0.018  0.1192 0.5    0.982 ]

# La sigmoide se satura: en los extremos su derivada es practicamente cero
# Se calcula en el mismo punto donde ya estaba evaluada: σ' = σ·(1 − σ)
print("derivada s(1-s):", np.round(sigmoide * (1 - sigmoide), 6))
# -> [0.002467 0.104994 0.25     0.104994 0.002467]
