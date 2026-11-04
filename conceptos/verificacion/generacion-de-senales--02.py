import numpy as np

# Ley fundamental: IR = IC * raiz(amplitud), con la amplitud = apuestas independientes al ano
ic, activos, dias = 0.03, 80, 252
amplitud = activos * dias
print("IC %.2f  amplitud %d  IR teorico %.2f" % (ic, amplitud, ic * np.sqrt(amplitud)))  # -> 4.26

# Si la senal se repite de un dia para otro, las apuestas no son independientes
for rho in (0.0, 0.5, 0.8, 0.9, 0.95):
    amplitud_ef = amplitud * (1 - rho) / (1 + rho)
    print("autocorr %4.2f  amplitud efectiva %8.0f  IR %.2f" % (rho, amplitud_ef, ic * np.sqrt(amplitud_ef)))

# El coste se come el IR: giro diario de 20 % del bruto y 4 pb por unidad de giro
giro_diario, coste_pb = 0.20, 4.0
coste_anual = giro_diario * dias * coste_pb / 1e4
print("coste anual estimado %.2f%% del capital bruto" % (100 * coste_anual))  # -> 2.02% del capital bruto
# -> IC 0.03  amplitud 20160  IR teorico 4.26
# -> autocorr 0.00  amplitud efectiva    20160  IR 4.26
# -> autocorr 0.50  amplitud efectiva     6720  IR 2.46
# -> autocorr 0.80  amplitud efectiva     2240  IR 1.42
# -> autocorr 0.90  amplitud efectiva     1061  IR 0.98
# -> autocorr 0.95  amplitud efectiva      517  IR 0.68
# -> coste anual estimado 2.02% del capital bruto
