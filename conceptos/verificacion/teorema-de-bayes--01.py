# Test medico: de la tasa de acierto a la probabilidad real de estar enfermo.
prevalencia = 0.01          # P(enfermo)
sensibilidad = 0.90         # P(positivo | enfermo)
especificidad = 0.95        # P(negativo | sano)

p_positivo = sensibilidad * prevalencia + (1 - especificidad) * (1 - prevalencia)
posterior = sensibilidad * prevalencia / p_positivo

print("P(positivo)          ", round(p_positivo, 4))    # salida: 0.0585
print("P(enfermo | positivo)", round(posterior, 4))     # salida: 0.1538
print("falsos positivos     ", round((1 - especificidad) * (1 - prevalencia), 4))  # salida: 0.0495
print("verdaderos positivos ", round(sensibilidad * prevalencia, 4))               # salida: 0.009
