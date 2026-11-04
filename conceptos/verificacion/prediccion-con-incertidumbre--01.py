import numpy as np

# Error del modelo frente al dato real, en el conjunto de calibración
pred = np.array([100, 100, 110, 96, 105, 120, 101, 99, 118, 95])
real = np.array([104, 96, 118, 89, 112, 131, 95, 107, 124, 88])
residuo_norm = np.abs(real - pred) / pred        # cuanto se desvia, en proporcion

# Cuantil empirico con redondeo hacia arriba, como en la prediccion conforme
q = np.quantile(residuo_norm, 0.80, method="higher")
q_abs = np.quantile(np.abs(real - pred), 0.80, method="higher")
print(f"q del error en %     {q:.4f}")           # -> 0.0808
print(f"q del error en unidades {q_abs:.2f}")    # -> 8.00

nueva = 115.0
lo, hi = nueva * (1 - q), nueva * (1 + q)
print(f"intervalo proporcional [{lo:.2f}, {hi:.2f}]")    # -> [105.71, 124.29]
print(f"intervalo en unidades  [{nueva - q_abs:.2f}, {nueva + q_abs:.2f}]")  # -> [107.00, 123.00]
