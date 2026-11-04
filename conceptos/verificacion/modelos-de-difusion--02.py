import numpy as np

T = 1000
abar = np.cumprod(1.0 - np.linspace(1e-4, 0.02, T))

# Al final de la cadena la senal es minima: un error pequeno en eps arruina la estimacion.
for t in (100, 500, 900, 990, 999):
    snr = abar[t] / (1 - abar[t])
    # sqrt((1 - abar) / abar) es el factor que multiplica al error de eps al despejar x0:
    # sale de dividir la formula de x_t entre sqrt(abar).
    ampl = np.sqrt((1 - abar[t]) / abar[t])
    print(f"t={t:>4}  SNR={snr:9.5f}  1/SNR={1 / snr:9.3f}"
          f"  error en x0 por 0.1 de error en eps={ampl * 0.1:8.3f}")
# -> t= 100  SNR=  8.53667  1/SNR=    0.117  error en x0 por 0.1 de error en eps=   0.034
# -> t= 500  SNR=  0.08436  1/SNR=   11.854  error en x0 por 0.1 de error en eps=   0.344
# -> t= 900  SNR=  0.00027  1/SNR= 3699.353  error en x0 por 0.1 de error en eps=   6.082
# -> t= 990  SNR=  0.00005  1/SNR=20672.767  error en x0 por 0.1 de error en eps=  14.378
# -> t= 999  SNR=  0.00004  1/SNR=24777.052  error en x0 por 0.1 de error en eps=  15.741
