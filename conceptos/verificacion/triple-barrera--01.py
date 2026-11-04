import numpy as np

precios = np.array([100.0, 100.5, 101.2, 102.4, 101.8,
                    99.9, 98.6, 99.4, 100.7, 101.5, 102.9, 103.4])
sigma = 0.02                  # volatilidad por barra (2 %), estimada solo con el pasado
pt, sl, h = 1.0, 1.0, 6       # multiplos de beneficio, de perdida y barrera vertical

def etiqueta_triple_barrera(precios, t0, sigma, pt, sl, h):
    """Devuelve la etiqueta y la barra en que queda determinada, t1."""
    p0 = precios[t0]
    arriba, abajo = p0 * (1 + pt * sigma), p0 * (1 - sl * sigma)
    for t in range(t0 + 1, min(t0 + h + 1, precios.size)):
        if precios[t] >= arriba:
            return 1, t
        if precios[t] <= abajo:
            return -1, t
    return 0, min(t0 + h, precios.size - 1)

# Dos eventos del mismo tramo: el de la barra 0 acaba en el objetivo y el de la 4 en el stop.
for t0 in (0, 4):
    etq, t1 = etiqueta_triple_barrera(precios, t0, sigma, pt, sl, h)
    print(f"t0={t0}  p0={precios[t0]:.1f}  barreras [{precios[t0]*(1-sl*sigma):.2f}, "
          f"{precios[t0]*(1+pt*sigma):.2f}]  etiqueta {etq:+d}  t1={t1}")

etiquetas = [etiqueta_triple_barrera(precios, t0, sigma, pt, sl, h)[0]
             for t0 in range(precios.size - 1)]
print("reparto de etiquetas:",
      {k: etiquetas.count(k) for k in (-1, 0, 1)})   # -> {-1: 3, 0: 3, 1: 5}
