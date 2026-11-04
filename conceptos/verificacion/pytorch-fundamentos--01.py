import numpy as np

# El bucle de entrenamiento, a mano y con NumPy, para ver que no hay magia.
x = np.array([[1.0], [2.0], [3.0], [4.0]])
y = np.array([[2.0], [4.0], [6.0], [8.0]])      # la relacion exacta es y = 2x
w, b, lr = np.zeros((1, 1)), 0.0, 0.1           # w se declara (1, 1) para que x @ w de (4, 1)

for paso in range(200):
    prediccion = x @ w + b                      # 1. hacia delante
    perdida = np.mean((prediccion - y) ** 2)    # 2. la perdida
    error = prediccion - y                      # 3. hacia atras, a mano
    # w -= ... modifica el array EN EL SITIO; w = w - ... crearia uno nuevo cada paso
    w -= lr * (2 * x.T @ error / len(x))        # 4. paso del optimizador
    b -= lr * (2 * error.mean())                # b es un float: aqui -= es solo reasignar
    if paso in (0, 99, 199):
        # :>3 alinea el numero del paso a la derecha y :8.4f reserva 8 caracteres para la perdida
        print(f"paso {paso:>3}  perdida {perdida:8.4f}  w {w[0, 0]:.4f}  b {b:+.4f}")
# -> paso   0  perdida  30.0000  w 3.0000  b +1.0000
# -> paso  99  perdida   0.0002  w 1.9901  b +0.0292
# -> paso 199  perdida   0.0000  w 1.9995  b +0.0014
