# Cuanto exagera un eje truncado, medido en pixeles.
def altura_px(valor, y_min, y_max, alto=200):
    return (valor - y_min) / (y_max - y_min) * alto

valores = [102, 105, 103, 107]
for etiqueta, y_min in [("desde 0  ", 0), ("desde 100", 100)]:
    alturas = [round(altura_px(v, y_min, max(valores) * 1.1 if y_min == 0 else 107.5)) for v in valores]
    print(f"eje {etiqueta}: alturas en px {alturas}  primera/ultima {alturas[0]/alturas[-1]:.2f}")
