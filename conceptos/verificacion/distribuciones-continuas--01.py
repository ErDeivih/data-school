from scipy import stats

# Probabilidades y cuantiles de las familias continuas mas usadas.
print(f"normal  P(-1 <= Z <= 1) = {stats.norm.cdf(1) - stats.norm.cdf(-1):.4f}")  # -> 0.6827
print(f"normal  P(Z <= 1.96)    = {stats.norm.cdf(1.96):.4f}")                    # -> 0.9750
print(f"t(5)    P(T <= 2.015)   = {stats.t.cdf(2.015, 5):.4f}")                   # -> 0.9500
print(f"t(5)    P(T <= 1.96)    = {stats.t.cdf(1.96, 5):.4f}")                    # -> 0.9464
print(f"t(30)   cuantil 0.975   = {stats.t.ppf(0.975, 30):.4f}")                 # -> 2.0423
print(f"chi2(3) cuantil 0.95    = {stats.chi2.ppf(0.95, 3):.4f}")                 # -> 7.8147
print(f"F(3,20) cuantil 0.95    = {stats.f.ppf(0.95, 3, 20):.4f}")                # -> 3.0984
print(f"exp(media 2) P(X <= 2)  = {stats.expon.cdf(2, scale=2):.4f}")             # -> 0.6321
