import numpy as np

# Visitas por dia de 4 semanas (filas = semanas, columnas = lunes a domingo).
visitas = np.array([[1200, 1150, 1250, 1300, 1100, 620, 540],
                    [1290, 1180, 1230, 1330, 1120, 660, 560],
                    [1150, 1200, 1270, 1290, 1150, 600, 520],
                    [ 980, 1190, 1250, 1310, 1130, 640, 550]])

referencia = visitas[:3]             # tres semanas de base
vigilada = visitas[3]                # la semana que se vigila
media_dia = referencia.mean(axis=0)  # una media por dia de la semana
sigma_dia = referencia.std(axis=0, ddof=1)

print("medias por dia (L a D):", media_dia.round(0).astype(int).tolist())
# -> [1213, 1177, 1250, 1307, 1123, 627, 540]
print("z de la semana vigilada:", ((vigilada - media_dia) / sigma_dia).round(2).tolist())
# -> [-3.29, 0.53, 0.0, 0.16, 0.26, 0.44, 0.5]
print("media global de las 21 observaciones:", round(referencia.mean()))
# -> 1034

# La misma caida del lunes, juzgada de dos formas: la media global la esconde.
z_lunes = (vigilada[0] - media_dia[0]) / sigma_dia[0]
z_global = (vigilada[0] - referencia.mean()) / referencia.std(ddof=1)
print(f"el lunes 980: z contra los lunes {z_lunes:.2f}, z contra todo {z_global:.2f}")
# -> el lunes 980: z contra los lunes -3.29, z contra todo -0.18
print("alerta solo con el mismo dia de la semana:", bool(abs(z_lunes) > 2))
# -> True
