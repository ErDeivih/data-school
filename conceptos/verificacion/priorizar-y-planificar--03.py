import numpy as np

# Capacidad: la nominal no es la real. El soporte, las incidencias y las entrevistas
# se comen una parte fija del sprint y no desaparecen porque el plan este lleno.
capacidad_nominal = 5 * 10          # 5 personas, 10 dias laborables
interrupcion = 0.30
planificable = capacidad_nominal * (1 - interrupcion)
print("capacidad planificable: %.0f personas-dia de %d" % (planificable, capacidad_nominal))
# -> capacidad planificable: 35 personas-dia de 50

# Cada tarea tarda entre 3 y 9 dias. Lo que se promete no es la media: es un percentil.
rng = np.random.default_rng(7)
for tareas in (4, 5, 6):
    totales = rng.integers(3, 10, size=(20_000, tareas)).sum(axis=1)
    cabe = 100 * float((totales <= planificable).mean())
    print("%d tareas -> p50 %2.0f, p80 %2.0f personas-dia, cabe en el sprint el %.0f %% de las veces"
          % (tareas, np.percentile(totales, 50), np.percentile(totales, 80), cabe))
# -> 5 tareas -> p50 30, p80 34 personas-dia, cabe en el sprint el 89 % de las veces
# -> 6 tareas -> p50 36, p80 40 personas-dia, cabe en el sprint el 46 % de las veces
