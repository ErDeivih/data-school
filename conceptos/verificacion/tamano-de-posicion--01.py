capital, riesgo = 50_000.0, 0.01        # 50 000 EUR y 1 % de riesgo por idea
entrada = 100.0

print(f"riesgo en euros {capital * riesgo:.0f}")     # -> riesgo en euros 500
for stop in (98.0, 96.0, 90.0):
    titulos = (capital * riesgo) / (entrada - stop)
    nocional = titulos * entrada
    print(f"stop {stop:>5.1f}  titulos {titulos:>6.1f}  nocional {nocional:>8.0f}  {nocional / capital:>6.1%}")
# -> stop  98.0  titulos  250.0  nocional    25000   50.0%
# -> stop  90.0  titulos   50.0  nocional     5000   10.0%
