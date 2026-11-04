# Simulacion de la prueba completa: objetivo, limite diario y drawdown movil.
def uniformes(semilla=987654321):
    x = semilla
    while True:                                # generador propio: deterministico y sin version
        x = (1103515245 * x + 12345) % (2 ** 31)
        yield x / 2 ** 31

def simular(riesgo, n_sim=2000, ops_dia=3, capital=100000.0,
            objetivo=6000.0, limite_diario=3000.0, perdida_max=6000.0, max_ops=400):
    azar = uniformes()
    aprueba = muere_dia = muere_total = 0
    ops_hasta = []
    for _ in range(n_sim):
        cap = pico = dia = capital
        ops = ops_hoy = 0
        while True:
            r = capital * riesgo
            cap += 2 * r if next(azar) < 0.45 else -r
            ops += 1
            ops_hoy += 1
            if cap - capital >= objetivo:              # exito
                aprueba += 1
                ops_hasta.append(ops)
                break
            if dia - cap >= limite_diario:             # el reloj diario corta
                muere_dia += 1
                break
            if pico - cap >= perdida_max:              # drawdown movil desde el maximo
                muere_total += 1
                break
            pico = max(pico, cap)
            if ops_hoy == ops_dia:                     # empieza un dia nuevo
                dia = cap
                ops_hoy = 0
            if ops >= max_ops:
                break
    mediana = sorted(ops_hasta)[len(ops_hasta) // 2]
    return aprueba / n_sim, muere_dia / n_sim, muere_total / n_sim, mediana

print("riesgo  aprueba  muere dia  muere total  mediana ops")
for riesgo in (0.0025, 0.005, 0.01, 0.02, 0.03):
    aprueba, dia, total, mediana = simular(riesgo)
    print(f"{riesgo:>6.2%}  {aprueba:>7.1%}  {dia:>9.1%}  {total:>11.1%}  {mediana:>11}")
