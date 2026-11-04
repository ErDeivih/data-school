import numpy as np

def purged_kfold(n_splits, t0, t1, embargo=0.0):
    """Divide en pliegues consecutivos y devuelve (train, test) con purga y embargo.

    t0, t1: arrays con el inicio y el fin de la etiqueta de cada observacion.
    embargo: fraccion del total de observaciones que se deja ciego tras el pliegue.
    """
    t0, t1 = np.asarray(t0, float), np.asarray(t1, float)
    assert np.all(t1 >= t0), "cada etiqueta debe terminar despues de empezar"
    n = t0.size
    pliegues = np.array_split(np.arange(n), n_splits)
    span = t1.max() - t0.min()

    for prueba in pliegues:
        inicio, fin = t0[prueba].min(), t1[prueba].max()

        # Purga: fuera cualquier etiqueta cuyo intervalo toque la ventana de prueba.
        solapa = (t1 >= inicio) & (t0 <= fin)

        # Embargo: fuera tambien el tramo inmediatamente posterior al pliegue.
        embargadas = (t0 > fin) & (t0 <= fin + embargo * span)

        entrenamiento = np.arange(n)[~solapa & ~embargadas]
        yield entrenamiento, prueba

# 100 observaciones cuyas etiquetas duran 10 pasos
n = 100
t0 = np.arange(n)
t1 = t0 + 10

for i, (train, test) in enumerate(purged_kfold(5, t0, t1, embargo=0.02)):
    print(f"pliegue {i}: prueba {test.size:>3}  train {train.size:>3}  "
          f"(purga+embargo quitan {n - test.size - train.size:>3})")
