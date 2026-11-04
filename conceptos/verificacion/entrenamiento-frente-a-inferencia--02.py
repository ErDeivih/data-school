import numpy as np

# Comparar el mismo dato transformado por los dos caminos: la prueba de coherencia
media, desviacion = 119.7723, 69.7077        # guardados con el modelo
control = np.array([80.0, 100.0, 119.7723, 150.0, 220.0])
z_entrenamiento = (control - media) / desviacion
z_produccion = (control - media) / desviacion       # misma funcion, mismos numeros
print("diferencia maxima %.2e" % np.max(np.abs(z_entrenamiento - z_produccion)))
# -> diferencia maxima 0.00e+00

# La version que falla: la constante escrita a mano en el servicio
otra_media = 100.0
z_mal = (control - otra_media) / desviacion
print("desplazamiento por variable %.4f" % np.max(np.abs(z_entrenamiento - z_mal)))
# -> desplazamiento por variable 0.2836
print("z correcto de 100 m2 %.4f   z con la media a mano %.4f"
      % (z_entrenamiento[1], z_mal[1]))
# -> z correcto de 100 m2 -0.2836   z con la media a mano 0.0000
