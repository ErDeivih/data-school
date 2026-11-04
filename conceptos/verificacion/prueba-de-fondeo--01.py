# La aritmetica de las reglas, antes de simular nada.
C = 100000.0
objetivo, limite_diario, perdida_max = 6000.0, 3000.0, 6000.0   # 6 %, 3 % y 6 %
p, R = 0.45, 2.0                                               # 45 % de acierto, gana el doble

for riesgo in (0.005, 0.01, 0.02):
    r = riesgo * C
    esperanza = r * (p * R - (1 - p))          # ganancia media por operacion
    print(f"riesgo {riesgo:.1%}: {r:>6.0f} EUR  esperanza {esperanza:>6.1f} EUR/op  "
          f"ops al objetivo {objetivo / esperanza:>5.1f}  "
          f"perdidas que caben al dia {limite_diario // r:.0f}  desde el maximo {perdida_max // r:.0f}")
