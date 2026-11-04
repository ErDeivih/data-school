from statsmodels.stats.power import TTestIndPower

# Cuanta muestra hace falta para detectar distintos efectos con desviacion 11,2.
analisis = TTestIndPower()
for delta in (6.2, 3.1, 1.55):
    n = analisis.solve_power(effect_size=delta / 11.2, alpha=0.05, power=0.80, ratio=1.0)
    print(f"delta {delta:>5.2f}  d {delta / 11.2:.3f}  n por grupo {n:>7.1f}")
    # -> delta  6.20  d 0.554  n por grupo    52.2
    # -> delta  3.10  d 0.277  n por grupo   205.9
    # -> delta  1.55  d 0.138  n por grupo   820.6
