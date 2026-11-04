import numpy as np

y = np.array([1.0, 0.0, 1.0])            # etiquetas reales
p = np.array([0.9, 0.2, 0.6])            # probabilidades predichas

# BCE: -log de la probabilidad que el modelo da a la clase verdadera
# En cada ejemplo solo sobrevive un sumando: el que corresponde a su etiqueta
bce = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
mse = np.mean((y - p) ** 2)

print(f"BCE {bce:.4f}")                   # -> BCE 0.2798
print(f"MSE {mse:.4f}")                   # -> MSE 0.0700

# Un error seguro y equivocado no se paga igual que uno tibio
print(f"-log(0.01) {-np.log(0.01):.3f}")  # -> -log(0.01) 4.605
print(f"-log(0.60) {-np.log(0.60):.3f}")  # -> -log(0.60) 0.511
