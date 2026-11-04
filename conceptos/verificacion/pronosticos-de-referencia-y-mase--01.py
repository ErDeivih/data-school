import numpy as np

# Serie mensual sintetica: 4 anos, ciclo anual fuerte (amplitud 20) y deriva suave (0,5 al mes).
azar = np.random.default_rng(3)
t = np.arange(48)
y = 100 + 0.5 * t + 20 * np.sin(2 * np.pi * t / 12) + azar.normal(0, 4, 48)

entrena, prueba = y[:36], y[36:]        # 3 anos para mirar, 1 ano para juzgar
h = np.arange(1, 13)                    # horizonte: de 1 a 12 meses por delante

# Los tres pronosticos de referencia para el ano que falta:
ingenuo = np.repeat(entrena[-1], 12)                                        # plano
estacional = entrena[-12:]                                                  # copia el ano anterior
deriva = entrena[-1] + h * (entrena[-1] - entrena[0]) / (len(entrena) - 1)  # sigue la recta

escala = np.abs(entrena[12:] - entrena[:-12]).mean()   # lo que falla el estacional en muestra
print("escala del MASE:", round(escala, 3))            # -> escala del MASE: 7.328
for nombre, f in (("ingenuo", ingenuo), ("estacional", estacional), ("deriva", deriva)):
    e = prueba - f
    mae, smape = np.abs(e).mean(), (2 * np.abs(e) / (np.abs(prueba) + np.abs(f))).mean()
    print(f"{nombre:11s} MAE {mae:6.3f}  MASE {mae / escala:5.3f}  sMAPE {smape:5.3f}")
# -> ingenuo     MAE 12.913  MASE 1.762  sMAPE 0.108
# -> estacional  MAE  5.466  MASE 0.746  sMAPE 0.047
# -> deriva     MAE 12.807  MASE 1.748  sMAPE 0.107
