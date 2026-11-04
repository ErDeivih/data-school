import numpy as np

# Calentamiento lineal + coseno, el plan tipico de un transformer pequeno.
def lr(paso, total=1000, calentamiento=100, lr_max=3e-4):
    if paso < calentamiento:
        return lr_max * paso / calentamiento          # subida lineal
    # El progreso se mide solo sobre lo que queda DESPUES del calentamiento, no sobre total
    progreso = (paso - calentamiento) / (total - calentamiento)
    return 0.5 * lr_max * (1 + np.cos(np.pi * progreso))

for paso in (0, 50, 100, 300, 600, 1000):
    # :>4 alinea a la derecha en 4 caracteres para que la columna no baile
    print(f"paso {paso:>4}  lr {lr(paso):.6f}")
# -> paso    0  lr 0.000000
# -> paso   50  lr 0.000150
# -> paso  100  lr 0.000300
# -> paso  300  lr 0.000265
# -> paso  600  lr 0.000124
# -> paso 1000  lr 0.000000
