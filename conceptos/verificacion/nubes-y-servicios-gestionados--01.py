import numpy as np

# Tres formas de conseguir el mismo computo: pagar por consulta, reservar capacidad fija
# o dejar que el proveedor escale por uso (sin servidor) hasta su techo de capacidad.
consulta = 6.0        # coste de cada 1000 consultas
reserva = 100.0       # cuota mensual fija de la capacidad reservada
techo = 150.0         # coste de consumo cuando el trafico llega al techo

q = np.array([10.0, 100.0, 500.0, 1000.0])     # consultas al mes, en miles
por_consulta = consulta * q
con_reserva = np.full_like(q, reserva)
sin_servidor = np.full_like(q, techo)           # el consumo ya esta en el techo a 700 mil
sin_servidor = np.where(q > 700, techo * (1 + 2.6 * (q - 700) / 300), sin_servidor)

total = np.vstack([por_consulta, con_reserva, sin_servidor])
for i, nombre in enumerate(("por consulta", "reservada   ", "sin servidor")):
    print(f"{nombre}  " + "  ".join(f"{v:8.1f}" for v in total[i]))
mas_barato = [("por consulta", "reservada", "sin servidor")[int(j)] for j in total.argmin(axis=0)]
print("mas barato en cada caso:", mas_barato)
# -> por consulta      60.0     600.0    3000.0    6000.0
# -> reservada        100.0     100.0     100.0     100.0
# -> sin servidor     150.0     150.0     150.0     540.0
# -> mas barato en cada caso: ['por consulta', 'reservada', 'reservada', 'reservada']
print(f"reservar gana a pagar por uso a partir de {reserva / consulta:.0f} mil consultas al mes")
# -> reservar gana a pagar por uso a partir de 17 mil consultas al mes
