# Cuántos tests independientes hacen falta para pasar de una previa del 1 % a más del 90 %.
prevalencia = 0.01
sensibilidad, especificidad = 0.90, 0.95

p = prevalencia
for test in range(1, 5):
    p = sensibilidad * p / (sensibilidad * p + (1 - especificidad) * (1 - p))
    print("tras", test, "test(s) positivos:", round(p, 4))

# salida:
# tras 1 test(s) positivos: 0.1538
# tras 2 test(s) positivos: 0.766
# tras 3 test(s) positivos: 0.9833
# tras 4 test(s) positivos: 0.9991
