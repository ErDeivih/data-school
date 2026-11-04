from scipy import stats

# Binomial: 10 ensayos independientes con la misma p = 0,3
n, p = 10, 0.3
print(f"P(X = 3)   = {stats.binom.pmf(3, n, p):.4f}")   # -> 0.2668
print(f"P(X <= 3)  = {stats.binom.cdf(3, n, p):.4f}")  # -> 0.6496
print(f"media bin  = {stats.binom.mean(n, p):.4f}")    # -> 3.0000
print(f"varianza   = {stats.binom.var(n, p):.4f}")     # -> 2.1000
print(f"P(X >= 8)  = {stats.binom.sf(7, n, p):.5f}")   # -> 0.00159

# Geometrica: numero de intentos hasta el primer exito, incluido el acierto
print(f"P(G = 5)   = {stats.geom.pmf(5, 0.2):.4f}")    # -> 0.0819
print(f"media geom = {stats.geom.mean(0.2):.4f}")      # -> 5.0000
