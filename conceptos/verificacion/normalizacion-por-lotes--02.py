import numpy as np

# El mismo valor se normaliza distinto segun el lote en el que caiga.
print(f"lote de 2     media {np.array([1.0, 2.0]).mean():.2f}  desviacion {np.array([1.0, 2.0]).std():.2f}")
# -> lote de 2     media 1.50  desviacion 0.50
grande = np.r_[np.full(999, 1.0), 3.0]   # np.full crea 999 unos y np.r_ los pega con el 3
print(f"lote de 1000  media {grande.mean():.3f}  desviacion {grande.std():.3f}")
# -> lote de 1000  media 1.002  desviacion 0.063

# Las estadisticas acumuladas arrancan sesgadas: es lo que se usa en inferencia.
media_movil = 0.0
for lote in (np.array([2.0, 4.0]), np.array([4.0, 6.0]), np.array([6.0, 8.0])):
    media_movil = 0.9 * media_movil + 0.1 * lote.mean()   # 0,9 y 0,1 son 1 - alfa y alfa
    print(f"lote de media {lote.mean():.1f}  media movil {media_movil:.3f}")
# -> lote de media 3.0  media movil 0.300
# -> lote de media 5.0  media movil 0.770
# -> lote de media 7.0  media movil 1.393
