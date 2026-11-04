import numpy as np

def sigmoide(x):
    return 1.0 / (1.0 + np.exp(-x))

def relu(x):
    # np.maximum compara elemento a elemento; el max() de Python no sabe hacerlo con un array
    return np.maximum(0.0, x)

# La aproximacion tanh de GELU, la que usan la mayoria de las implementaciones
def gelu(x):
    return 0.5 * x * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (x + 0.044715 * x**3)))

x = np.array([-6.0, -2.0, 0.0, 2.0, 6.0])
print("entradas ", x)                          # -> [-6. -2.  0.  2.  6.]
print("sigmoide ", np.round(sigmoide(x), 4))   # -> [0.0025 0.1192 0.5    0.8808 0.9975]
print("tanh     ", np.round(np.tanh(x), 4))    # -> [-1.    -0.964  0.     0.964  1.   ]
print("relu     ", np.round(relu(x), 4))       # -> [0. 0. 0. 2. 6.]
print("gelu     ", np.round(gelu(x), 4))       # -> [-0.     -0.0454  0.      1.9546  6.    ]
