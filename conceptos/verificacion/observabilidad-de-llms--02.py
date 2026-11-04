# El coste por traza: lo que cuesta la cola y de que esta hecha la factura.
import numpy as np

rng = np.random.default_rng(7)
N = 500
reintentos = rng.binomial(2, 0.30, size=N)

P_ENTRADA, P_CACHE, P_SALIDA = 3.00, 0.30, 15.00        # euros por millon de tokens
TEXTO_ENTRADA = rng.integers(1_400, 2_200, size=N)      # instrucciones, historial y pregunta
DOCUMENTOS = rng.integers(0, 8, size=N)                 # recuperados por consulta
TOKENS_POR_DOCUMENTO, TOKENS_SALIDA = 420, 250

tokens_entrada = TEXTO_ENTRADA + DOCUMENTOS * TOKENS_POR_DOCUMENTO + reintentos * 3_600
# El prefijo estable (instrucciones mas catalogo) se cobra a precio de cache.
tokens_cache = np.full(N, 1_200)
coste = (tokens_entrada * P_ENTRADA + tokens_cache * P_CACHE
         + TOKENS_SALIDA * P_SALIDA) / 1e6

mediana = float(np.median(coste))
p95 = float(np.percentile(coste, 95))
print("coste mediano por consulta:", round(mediana, 4), "EUR")
print("coste del p95:", round(p95, 4), "EUR")
print("el p95 cuesta", round(p95 / mediana, 2), "veces la mediana")
print("factura del dia:", round(float(coste.sum()), 2), "EUR")
# -> coste mediano por consulta: 0.0206 EUR
# -> coste del p95: 0.0346 EUR
# -> el p95 cuesta 1.68 veces la mediana
# -> factura del dia: 10.37 EUR

# La cola no es un caso raro: es un grupo de consultas que se puede aislar y arreglar.
orden = np.argsort(coste)                                 # de mas barata a mas cara
cola = int(0.05 * N)
print("la cola del 5 % mas caro se lleva:",
      round(float(coste[orden][-cola:].sum() / coste.sum()), 4))
print("la cola del 5 % mas caro cuesta de media:",
      round(float(coste[orden][-cola:].mean()), 4), "EUR por consulta")
print("la mitad mas barata de la factura cabe en",
      int(np.searchsorted(np.cumsum(coste[orden]) / coste.sum(), 0.5)) + 1, "consultas")
# -> la cola del 5 % mas caro se lleva: 0.0917
# -> la cola del 5 % mas caro cuesta de media: 0.038 EUR por consulta
# -> la mitad mas barata de la factura cabe en 321 consultas

# Y el desglose por partida: que concepto se come el presupuesto.
total = (tokens_entrada * P_ENTRADA + tokens_cache * P_CACHE + TOKENS_SALIDA * P_SALIDA).sum() / 1e6
for nombre, euros in (("entrada", (tokens_entrada * P_ENTRADA).sum() / 1e6),
                      ("cache", (tokens_cache * P_CACHE).sum() / 1e6),
                      ("salida", (TOKENS_SALIDA * P_SALIDA * N) / 1e6)):
    print(f"{nombre:8s} {euros:6.2f} EUR al dia   {euros / total:5.1%}")
# -> entrada    8.31 EUR al dia   80.2%
# -> cache      0.18 EUR al dia    1.7%
# -> salida     1.88 EUR al dia   18.1%
