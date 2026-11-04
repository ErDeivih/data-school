# La exactitud que no hay que vender: un problema con un 1 % de casos positivos.
n = 10000
positivos = 100                    # 1 % de los casos; el resto son negativos
vp, fn, fp, vn = 60, 40, 90, 9810  # matriz de confusion del modelo

exactitud = (vp + vn) / n
sensibilidad = vp / (vp + fn)      # de los positivos reales, cuantos detecta
precision = vp / (vp + fp)         # de los que marca, cuantos lo son

print(f"el que dice siempre 'no' acierta {(n - positivos) / n:.2%}")  # -> 99.00%
print(f"exactitud {exactitud:.2%}")        # -> 98.70%
print(f"sensibilidad {sensibilidad:.2%}")  # -> 60.00%
print(f"precision {precision:.2%}")        # -> 40.00%
