import numpy as np

# 1000 viviendas: superficie lognormal y precio = 1.2 * superficie + ruido
azar = np.random.default_rng(3)
n = 1000
area = azar.lognormal(4.6, 0.55, n)
precio = 1.2 * area + azar.normal(0.0, 8.0, n)
corte = 700

# Los estadisticos se calculan SOLO con el entrenamiento y se guardan con el modelo
media, desviacion = area[:corte].mean(), area[:corte].std()
z = (area - media) / desviacion

# El modelo se entrena sobre la variable ya estandarizada
ejes = np.column_stack([np.ones(corte), z[:corte]])
pesos = np.linalg.lstsq(ejes, precio[:corte], rcond=None)[0]
print("pesos: %.4f y %.4f" % (pesos[0], pesos[1]))
# -> pesos: 144.2564 y 83.8899
print("media del entrenamiento %.4f  desviacion %.4f" % (media, desviacion))
# -> media del entrenamiento 119.7723  desviacion 69.7077

# --- Camino correcto: al servir se usan los estadisticos guardados ------------
z_ok = z[corte:]
pred_ok = pesos[0] + pesos[1] * z_ok
print("MAE con los estadisticos del entrenamiento %.3f"
      % np.mean(np.abs(precio[corte:] - pred_ok)))
# -> MAE con los estadisticos del entrenamiento 6.646

# --- El error: al servir se recalculan con el lote que llega ------------------
media_lote = area[corte:].mean()
print("media del lote %.4f  desplazamiento %.2f desviaciones  %.2f de precio"
      % (media_lote, (media_lote - media) / desviacion,
         pesos[1] * (media_lote - media) / desviacion))
# -> media del lote 114.6565  desplazamiento -0.07 desviaciones  -6.16 de precio
z_mal = (area[corte:] - media_lote) / area[corte:].std()
pred_mal = pesos[0] + pesos[1] * z_mal
print("MAE con los estadisticos del lote %.3f" % np.mean(np.abs(precio[corte:] - pred_mal)))
# -> MAE con los estadisticos del lote 9.264
