import numpy as np

real = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
gen = np.array([[0.05, 0.05], [0.95, 0.05], [0.5, 0.9]])
radio = 0.35

d_gen_real = np.linalg.norm(gen[:, None, :] - real[None, :, :], axis=2)
precision = (d_gen_real.min(axis=1) <= radio).mean()

d_real_gen = np.linalg.norm(real[:, None, :] - gen[None, :, :], axis=2)
recall = (d_real_gen.min(axis=1) <= radio).mean()

print(f"precision {precision:.4f}")                          # -> 0.6667
print(f"recall    {recall:.4f}")                             # -> 0.5000
print("puntos generados fuera:", int((d_gen_real.min(axis=1) > radio).sum()))    # -> 1
print("puntos reales sin cubrir:", int((d_real_gen.min(axis=1) > radio).sum()))  # -> 2
