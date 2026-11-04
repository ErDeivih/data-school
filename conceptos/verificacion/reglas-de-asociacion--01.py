import numpy as np

tickets = 1000
pan, mantequilla, pan_y_mantequilla = 200, 100, 80
leche, pan_y_leche, cafe, azucar, cafe_y_azucar = 300, 30, 600, 500, 400

def regla(n_xy, n_x, n_y, total):
    """n_xy: cestas con los dos; n_x: con el antecedente; n_y: con el consecuente."""
    soporte = n_xy / total
    confianza = n_xy / n_x
    lift = confianza / (n_y / total)         # compara con el azar, no con el antecedente
    return soporte, confianza, lift

for nombre, args in [("pan -> mantequilla", (pan_y_mantequilla, pan, mantequilla, tickets)),
                     ("cafe -> azucar", (cafe_y_azucar, cafe, azucar, tickets)),
                     ("pan -> leche", (pan_y_leche, pan, leche, tickets))]:
    s, c, l = regla(*args)                   # *args reparte la tupla en los cuatro argumentos
    print(f"{nombre:18s} soporte {s:.3f}  confianza {c:.3f}  lift {l:.3f}")
# -> pan -> mantequilla soporte 0.080  confianza 0.400  lift 4.000
# -> cafe -> azucar     soporte 0.400  confianza 0.667  lift 1.333
# -> pan -> leche       soporte 0.030  confianza 0.150  lift 0.500
