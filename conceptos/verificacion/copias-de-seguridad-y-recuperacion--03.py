# La retencion pesa mas que la frecuencia: nadie guarda 365 copias completas.
completa_gb, incremental_gb = 400, 30
diarias, semanales, mensuales = 7, 4, 12

gfs = diarias * incremental_gb + (semanales + mensuales) * completa_gb
diario_completo = 365 * completa_gb
print("abuelo-padre-hijo: %6.0f GB" % gfs)                    # ->   6610 GB
print("365 copias completas: %6.0f GB" % diario_completo)     # -> 146000 GB
print("factor de ahorro: %.0f x" % (diario_completo / gfs))   # -> 22 x
