# Medir en vez de suponer: la cuantizacion se evalua. Este bloque compara una senal
# sintetica de calidad y de velocidad para dejar claro que las dos se miden juntas.
import numpy as np

rng = np.random.default_rng(3)

# "Calidad": la discrepancia entre lo que daria un modelo de referencia y lo que da el
# cuantizado. Aqui se simula con ruido proporcional a lo agresivo del formato.
FORMATOS = {"16 bits": (0.000, 1.00), "8 bits": (0.010, 1.28), "4 bits": (0.045, 1.60)}

print("formato   error_medio   acierto   tokens_por_segundo")
for nombre, (ruido, factor) in FORMATOS.items():
    referencia = rng.normal(1.0, 0.30, size=2_000)
    cuantizado = referencia + rng.normal(0.0, ruido, size=2_000)
    error = float(np.abs(cuantizado - referencia).mean())
    # El acierto se simula como la fraccion de casos que quedan dentro de una tolerancia.
    acierto = float((np.abs(cuantizado - referencia) < 0.05).mean())
    print(f"{nombre:9s} {error:11.4f}   {acierto:7.3f}   {69.0 * factor:17.1f}")
# -> formato   error_medio   acierto   tokens_por_segundo
# -> 16 bits      0.0000     1.000                69.0
# -> 8 bits       0.0080     1.000                88.3
# -> 4 bits       0.0362     0.736               110.4

# La decision no sale de la tabla sola: hay un umbral de acierto por debajo del cual
# el ahorro de velocidad no compensa. Aqui, el 90 %.
UMBRAL_ACIERTO = 0.90
for nombre, (ruido, factor) in FORMATOS.items():
    referencia = rng.normal(1.0, 0.30, size=2_000)
    cuantizado = referencia + rng.normal(0.0, ruido, size=2_000)
    acierto = float((np.abs(cuantizado - referencia) < 0.05).mean())
    velocidad = 69.0 * factor
    print(f"{nombre:9s} acierto {acierto:5.3f}  velocidad {velocidad:5.1f}  "
          f"{'vale' if acierto >= UMBRAL_ACIERTO else 'no vale: se pierde calidad'}")
# -> 16 bits acierto 1.000  velocidad  69.0  vale
# ->  8 bits acierto 1.000  velocidad  88.3  vale
# ->  4 bits acierto 0.723  velocidad 110.4  no vale: se pierde calidad
