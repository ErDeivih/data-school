# Coste de un preentrenamiento: C ~ 6 * N * D (N parametros, D tokens)
N = 1.0e9        # parametros
D = 2.0e10       # tokens
C = 6 * N * D    # FLOPs totales

# Supuesto explicito: 3.0e14 FLOP/s utiles sostenidos por GPU (no es un benchmark medido)
flops_por_segundo = 3.0e14
horas = C / flops_por_segundo / 3600    # de segundos a horas: 3600 s por hora

print(f"FLOPs totales      {C:.3e}")          # -> 1.200e+20
print(f"horas en una GPU   {horas:.1f}")      # -> 111.1
print(f"horas en 64 GPUs   {horas / 64:.2f}") # -> 1.74

# Con la regla de ~20 tokens por parametro, el reparto para un presupuesto dado:
presupuesto = 1.0e20
n_opt = (presupuesto / (6 * 20)) ** 0.5    # despeja N de C = 6 * N * (20 * N) = 120 * N^2
print(f"para {presupuesto:.0e} FLOPs -> N = {n_opt:.3e} parametros, D = {20 * n_opt:.3e} tokens")
# -> N = 9.129e+08 parametros, D = 1.826e+10 tokens
