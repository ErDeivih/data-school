import pandas as pd

# Cuatro cohortes de usuarios nuevos y su actividad en las semanas siguientes.
# Cada fila es una cohorte; cada columna, una semana desde el alta (0 = el alta).
retencion = pd.DataFrame(
    [[1000, 420, 300, 250, 230],
     [1200, 456, 312, 210, None],
     [1400, 476, 308, None, None],
     [1600, 496, None, None, None]],
    index=["2024-01", "2024-02", "2024-03", "2024-04"],
    columns=[0, 1, 2, 3, 4])

# Curva de retencion: activos de la semana t sobre el tamano inicial de esa cohorte.
curva = retencion.div(retencion[0], axis=0)
print((100 * curva).round(1))
print("semana 2 por cohorte:", [round(100 * float(v), 1) for v in curva[2].dropna()])
# -> semana 2 por cohorte: [30.0, 26.0, 22.0]

# El agregado engana: juntar todas las cohortes mezcla usuarios de edades distintas.
usuarios = int(retencion[0].sum())
print("activos sobre el total por semana:",
      [round(100 * float(retencion[s].sum()) / usuarios, 1) for s in retencion.columns])
# -> activos sobre el total por semana: [100.0, 35.5, 17.7, 8.8, 4.4]
