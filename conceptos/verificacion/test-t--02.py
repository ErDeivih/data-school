import numpy as np
from scipy import stats

# Las mismas 8 personas medidas antes y despues: los datos estan apareados.
antes = np.array([210, 195, 230, 205, 220, 200, 215, 225], float)
despues = np.array([200, 188, 219, 197, 214, 191, 208, 216], float)

tp, pp = stats.ttest_rel(antes, despues)
ti, pi = stats.ttest_ind(antes, despues, equal_var=False)   # Welch, por si acaso

print(f"pareado     t {tp:+.2f}  p {pp:.2e}")     # -> pareado     t +14.06  p 2.18e-06
print(f"independ.   t {ti:+.2f}  p {pi:.4f}")     # -> independ.   t +1.39  p 0.1854
print(f"sd entre personas {antes.std(ddof=1):.2f}")  # -> sd entre personas 12.25
