import numpy as np

# Un ano, 50.000 trayectorias: media del logaritmo frente a la media simple
rng = np.random.default_rng(11)
mu, sigma, reps = 0.08, 0.30, 50_000

log_r = (mu - 0.5 * sigma ** 2) + sigma * rng.standard_normal(reps)
simple = np.exp(log_r) - 1

print(f"media log {log_r.mean():.4f}")          # -> media log 0.0346
print(f"teorica {mu - 0.5 * sigma ** 2:.4f}")   # -> teorica 0.0350
print(f"media simple {simple.mean():.4f}")      # -> media simple 0.0827
print(f"exp(mu)-1 {np.exp(mu) - 1:.4f}")        # -> exp(mu)-1 0.0833