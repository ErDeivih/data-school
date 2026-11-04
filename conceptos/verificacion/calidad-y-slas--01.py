import numpy as np

# Retraso en minutos sobre las 06:30 de la particion diaria, ultimos 30 dias.
retrasos = np.array([0, 2, 0, 5, 0, 0, 3, 0, 12, 0, 0, 4, 0, 0, 8, 0,
                     0, 0, 6, 0, 0, 2, 0, 0, 40, 0, 0, 3, 0, 0])

umbral, slo = 30, 0.99
cumplimiento = (retrasos <= umbral).mean()
presupuesto = (1 - slo) * retrasos.size
print(f"cumplimiento {cumplimiento:.1%}")                       # -> cumplimiento 96.7%
print(f"dias observados {retrasos.size}  fuera {int((retrasos > umbral).sum())}")  # -> dias observados 30  fuera 1
print(f"presupuesto de error {presupuesto:.1f} dias")           # -> presupuesto de error 0.3 dias
print(f"mediana {np.median(retrasos):.1f} min  p95 {np.percentile(retrasos, 95):.1f} min")
# -> mediana 0.0 min  p95 10.2 min
