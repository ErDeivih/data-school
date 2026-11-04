import numpy as np

n_estados, meta = 6, 5          # pasillo 0..5; en 5 esta la meta
rng = np.random.default_rng(0)


def paso(s, a):
    s2 = min(max(s + (1 if a == 1 else -1), 0), n_estados - 1)   # 1 = derecha
    return s2, (0.0 if s2 == meta else -1.0)                     # -1 por cada paso


Q = np.zeros((n_estados, 2))
alpha, gamma, epsilon = 0.5, 0.9, 0.2
for _ in range(500):
    s = 0
    for _ in range(50):
        a = int(rng.integers(2)) if rng.random() < epsilon else int(np.argmax(Q[s]))
        s2, recompensa = paso(s, a)
        Q[s, a] += alpha * (recompensa + gamma * Q[s2].max() - Q[s, a])   # error TD
        s = s2
        if s == meta:
            break

print("estado   Q(izquierda)   Q(derecha)")
for s in range(meta):
    print(f"{s:>6}   {Q[s, 0]:12.3f}   {Q[s, 1]:9.3f}")
# -> estado   Q(izquierda)   Q(derecha)
# ->      0         -4.095      -3.439
# ->      1         -4.095      -2.710
# ->      2         -3.439      -1.900
# ->      3         -2.710      -1.000
# ->      4         -1.900       0.000

s, pasos = 0, 0
while s != meta and pasos < 20:
    s, _ = paso(s, int(np.argmax(Q[s])))
    pasos += 1
print(f"pasos desde el estado 0 con la politica greedy: {pasos}")
# -> pasos desde el estado 0 con la politica greedy: 5
