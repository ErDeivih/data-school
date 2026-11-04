# El orden de las etapas decide cuanto tarda un desarrollador en saber que ha roto algo.
etapas = {"e2e": (600, 0.05), "integracion": (240, 0.15),
          "unitarias": (40, 0.25), "lint": (5, 0.02)}

def espera_hasta_fallo(orden):
    """Media del tiempo hasta la primera etapa que falla, condicionada a que algo falle."""
    total, llega, acumulado = 0.0, 1.0, 0
    for nombre in orden:
        duracion, p_fallo = etapas[nombre]        # desempaqueta la tupla (segundos, probabilidad)
        acumulado += duracion                     # lo que se lleva esperado al llegar aqui
        # Solo suma si la ejecucion llego hasta esta etapa: de ahi el factor `llega`.
        total += llega * p_fallo * acumulado
        llega *= 1 - p_fallo                      # probabilidad de pasar a la siguiente
    return total / (1 - llega)          # normalizamos por la probabilidad de fallar

actual = ["e2e", "integracion", "unitarias", "lint"]
# sorted SIN reverse: pone delante la etapa con menor coste por unidad de probabilidad de fallo.
mejor = sorted(etapas, key=lambda n: etapas[n][0] / etapas[n][1])

print(f"orden actual          {espera_hasta_fallo(actual):7.1f} s")   # ->   831.7 s
print(f"orden por coste/fallo {espera_hasta_fallo(mejor):7.1f} s")   # ->   171.6 s
print("orden propuesto:", " ".join(mejor))          # -> unitarias lint integracion e2e
# El guion bajo del generador descarta la probabilidad: la duracion total no depende del orden.
print("duracion si todo pasa:", sum(d for d, _ in etapas.values()), "s")   # -> 885 s
