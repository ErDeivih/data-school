# Agregados de una traza: lo minimo que hay que grabar para poder depurar y presupuestar.
import numpy as np

rng = np.random.default_rng(7)
N = 500

# Reintentos de cada consulta: la causa principal de la cola de latencia.
reintentos = rng.binomial(2, 0.30, size=N)
# El exito depende del numero de reintentos: mas intentos, sistema mas nervioso.
exito = rng.random(N) < np.where(reintentos == 0, 0.96, np.where(reintentos == 1, 0.90, 0.75))
# La latencia base de una llamada, con cola (lognormal), mas el coste de cada reintento.
latencia = rng.lognormal(mean=np.log(1100.0), sigma=0.35, size=N) + reintentos * 1900 \
           + np.where(exito, 0.0, 2500.0)

print("traza   exito   reintentos   latencia_ms")
for i in (0, 1, 2):
    print(f"{i:5d}   {str(bool(exito[i])):5s}   {reintentos[i]:10d}   {latencia[i]:11.0f}")
print("p50 de latencia:", round(float(np.percentile(latencia, 50))), "ms")
print("p95 de latencia:", round(float(np.percentile(latencia, 95))), "ms")
print("exito:", round(float(exito.mean()), 4))
# -> traza   exito   reintentos   latencia_ms
# ->     0   True             1          2536
# ->     1   True             1          2990
# ->     2   True             1          3209
# -> p50 de latencia: 2643 ms
# -> p95 de latencia: 5312 ms
# -> exito: 0.918

# La media de latencia no describe a nadie: mira la distancia entre la mediana y el p95.
print("media", round(float(latencia.mean())), "ms   p95 - p50:",
      round(float(np.percentile(latencia, 95) - np.percentile(latencia, 50))), "ms")
# -> media 2559 ms   p95 - p50: 2668 ms
