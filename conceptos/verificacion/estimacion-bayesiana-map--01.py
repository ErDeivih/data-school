import numpy as np
from scipy import stats

# Mismo problema de la moneda, con una prior Beta(3, 3) centrada en 0,5
caras, cruces = 7, 3
alpha_prior, beta_prior = 3.0, 3.0

# La posterior es Beta(alpha + caras, beta + cruces): conjugada con la binomial
a_post, b_post = alpha_prior + caras, beta_prior + cruces
grid = np.linspace(1e-9, 1 - 1e-9, 200_001)
posterior = stats.beta.pdf(grid, a_post, b_post)

map_ = grid[np.argmax(posterior)]
media_post = a_post / (a_post + b_post)
mle = caras / (caras + cruces)

print(f"MLE          {mle:.3f}")          # -> 0.700
print(f"MAP          {map_:.3f}")         # -> 0.643
print(f"media post.  {media_post:.3f}")   # -> 0.625
print(f"IC 95 % creible [{stats.beta.ppf(0.025, a_post, b_post):.3f}, {stats.beta.ppf(0.975, a_post, b_post):.3f}]")  # -> [0.384, 0.837]
