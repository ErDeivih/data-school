import numpy as np

recompensas = np.array([0.0, 0.0, -1.0, 0.0, 10.0])
gamma = 0.9

# El retorno se calcula de atras hacia delante: G_t = r_t + gamma * G_{t+1}.
G = np.zeros_like(recompensas)
acumulado = 0.0
for t in range(len(recompensas) - 1, -1, -1):
    acumulado = recompensas[t] + gamma * acumulado
    G[t] = acumulado

for t in range(len(recompensas)):
    print(f"t={t}  r={recompensas[t]:>5}  retorno descontado G_t={G[t]:.4f}")
# -> t=0  r=  0.0  retorno descontado G_t=5.7510
# -> t=1  r=  0.0  retorno descontado G_t=6.3900
# -> t=2  r= -1.0  retorno descontado G_t=7.1000
# -> t=3  r=  0.0  retorno descontado G_t=9.0000
# -> t=4  r= 10.0  retorno descontado G_t=10.0000

print(f"G_0 a mano: -0.9^2 + 10 * 0.9^4 = {-0.9 ** 2 + 10 * 0.9 ** 4:.4f}")
# -> G_0 a mano: -0.9^2 + 10 * 0.9^4 = 5.7510
