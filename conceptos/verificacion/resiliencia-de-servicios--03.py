# La disponibilidad se compone: en serie se multiplica, en paralelo se mejora.
disponibilidades = [0.999, 0.999, 0.99]      # pagos, catalogo, antifraude
en_serie = 1.0
for a in disponibilidades:
    en_serie *= a
print("tres dependencias en serie: %.5f" % en_serie)            # -> 0.98802
print("horas de degradacion al mes: %.1f" % ((1 - en_serie) * 720))  # -> 8.6

# Replicas en paralelo: solo mejora si el fallo es independiente y hay capacidad.
for n in (1, 2, 3):
    print("%d replica(s) al 99 %%: %.6f" % (n, 1 - (1 - 0.99) ** n))
# -> 2 replica(s) al 99 %: 0.999900
# -> 3 replica(s) al 99 %: 0.999999
