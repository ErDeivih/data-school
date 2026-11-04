import statistics

# Series propias con un generador congruencial, para que el ejemplo no dependa
# de la version de la libreria ni de la semilla de un generador ajeno.
def uniformes(n, semilla=12345):
    x, salida = semilla, []
    for _ in range(n):
        x = (1103515245 * x + 12345) % (2 ** 31)
        salida.append(x / 2 ** 31)
    return salida

u = uniformes(120)
r_eq = [0.008 + 0.045 * (2 * x - 1) for x in u[:60]]   # bolsa: en torno al 0,8 % mensual
r_bd = [0.002 + 0.006 * (2 * x - 1) for x in u[60:]]   # bonos: en torno al 0,2 % mensual

def simular(politica, umbral=0.05, coste=0.001):
    v_eq, v_bd, ops, pagado = 60000.0, 40000.0, 0, 0.0
    pico, caida, retornos = 100000.0, 0.0, []
    for t in range(60):
        inicio = v_eq + v_bd
        v_eq *= (1 + r_eq[t])
        v_bd *= (1 + r_bd[t])
        total = v_eq + v_bd
        if (politica == "anual" and t % 12 == 11) or \
           (politica == "umbral" and abs(v_eq / total - 0.60) >= umbral):
            negociado = abs(0.60 * total - v_eq)       # notional que cambia de manos
            total -= negociado * coste                 # el coste sale de la cartera
            v_eq, v_bd = 0.60 * total, 0.40 * total
            ops += 1
            pagado += negociado * coste
        retornos.append((v_eq + v_bd) / inicio - 1)
        pico = max(pico, v_eq + v_bd)
        caida = max(caida, 1 - (v_eq + v_bd) / pico)
    return v_eq + v_bd, retornos, caida, ops, pagado

print(f"{'politica':>16} {'valor final':>12} {'vol mensual':>12} {'caida max':>10} {'ops':>5} {'coste':>8}")
for politica, nombre in (("nada", "sin rebalancear"), ("anual", "anual"), ("umbral", "umbral 5 pp")):
    valor, rets, caida, ops, pagado = simular(politica)
    print(f"{nombre:>16} {valor:>12,.0f} {statistics.stdev(rets):>12.4f} {caida:>10.4f} {ops:>5} {pagado:>8.2f}")
