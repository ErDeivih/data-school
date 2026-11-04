import numpy as np

# Perdida DPO: -ln sigma(beta * [(ln pi_w - ln ref_w) - (ln pi_l - ln ref_l)])
sigma = lambda z: 1 / (1 + np.exp(-z))

beta = 0.1
log_ratio_w, log_ratio_l = 0.5, -0.2        # cuanto ha subido cada respuesta respecto al modelo base

margen = beta * (log_ratio_w - log_ratio_l)   # margen ya escalado por beta, como en la formula
print(f"margen {margen:+.3f}  perdida {-np.log(sigma(margen)):.4f}")   # -> margen +0.070  perdida 0.6588

# Si la respuesta peor sube mas que la buena, el margen se vuelve negativo y la perdida crece
for lw, ll in [(0.5, -0.2), (0.2, 0.9), (-0.3, -0.1)]:
    m = beta * (lw - ll)      # el mismo calculo que arriba, con los tres pares del ejemplo
    print(f"log-ratios ({lw:+.1f}, {ll:+.1f})  margen {m:+.3f}  perdida {-np.log(sigma(m)):.4f}")
# -> margenes +0.070, -0.070 y -0.020 con perdidas 0.6588, 0.7288 y 0.7032
