# Calcular una media en MapReduce: cada particion emite (suma, cuenta), no su media.
particiones = [[10, 20, 30], [40, 50], [60]]

medias = [sum(p) / len(p) for p in particiones]
media_de_medias = sum(medias) / len(medias)

suma_total = sum(sum(p) for p in particiones)
cuenta_total = sum(len(p) for p in particiones)
media_correcta = suma_total / cuenta_total

print("medias por particion:", medias)                       # -> [20.0, 45.0, 60.0]
print("media de medias: {:.2f}".format(media_de_medias))     # -> 41.67
print("media correcta:  {:.2f}".format(media_correcta))      # -> 35.00
