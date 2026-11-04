# Repintado: decidir con la barra en formacion o esperar a que cierre.
ticks = [100.0, 100.5, 99.5, 100.2, 100.3, 101.0, 101.2, 100.4]
fin_barra = [4, 6, 8]
barras = [ticks[a:b] for a, b in zip([0] + fin_barra[:-1], fin_barra)]
cierres = [b[-1] for b in barras]
umbral = cierres[0]

entrada_formacion = next(t for t in barras[1] if t > umbral)   # mira la vela a medias
entrada_confirmada = barras[2][0]                             # espera al cierre
salida = cierres[2]

print("cierres de barra:", cierres)                    # -> [100.2, 101.0, 100.4]
print(f"barra en formacion  entrada {entrada_formacion:.1f}  resultado {salida / entrada_formacion - 1:+.2%}")
# -> barra en formacion  entrada 100.3  resultado +0.10%
print(f"barra cerrada       entrada {entrada_confirmada:.1f}  resultado {salida / entrada_confirmada - 1:+.2%}")
# -> barra cerrada       entrada 101.2  resultado -0.79%
