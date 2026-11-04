# Calculo de la espera entre reintentos: exponencial y con jitter
import random

random.seed(0)                      # semilla fija: el ejemplo es reproducible

t_base, t_max = 0.5, 30.0
for intento in range(5):
    espera = min(t_max, t_base * 2 ** intento)
    con_jitter = espera * (1 + random.random())
    print(f"intento {intento}: espera base {espera:>4.1f}s  con jitter {con_jitter:>5.2f}s")
