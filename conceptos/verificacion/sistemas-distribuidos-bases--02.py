# Los relojes de dos maquinas no avanzan igual: el desfase crece mientras nadie sincronice.
desfase_ppm = 100                      # 100 partes por millon
for horas in (1, 24, 24 * 7):
    # ppm son millonésimas: 100 ppm son 100 microsegundos por segundo, o 0,36 s por hora.
    print(f"{horas:>4} h -> {desfase_ppm * horas * 3600 / 1e6:7.2f} s de desfase")

print(f"en un dia: {desfase_ppm * 24 * 3600 / 1e6:.2f} s")   # -> 8.64 s
sincronizado = desfase_ppm * 64 / 1e6 * 1000     # resincronizando cada 64 s
# El * 1000 final convierte los segundos en milisegundos: sin el, la cifra no se lee.
print(f"resincronizando cada 64 s: {sincronizado:.1f} ms de desfase esperado")   # -> 6.4 ms
