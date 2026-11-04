from scipy import stats

# Binomial con n grande y p pequena: el limite es la Poisson con lambda = n * p.
n, p = 10000, 0.00025
print(f"binomial P(X = 0) = {stats.binom.pmf(0, n, p):.5f}")   # -> 0.08206
print(f"Poisson  P(N = 0) = {stats.poisson.pmf(0, n * p):.5f}")   # -> 0.08208
print(f"binomial P(X = 2) = {stats.binom.pmf(2, n, p):.5f}")   # -> 0.25654
print(f"Poisson  P(N = 2) = {stats.poisson.pmf(2, n * p):.5f}")   # -> 0.25652
print(f"lambda = n * p    = {n * p}")                          # -> 2.5

# La cola de la Poisson: sucesos raros que en volumen anual dejan de serlo.
print(f"Poisson P(N >= 8) = {stats.poisson.sf(7, n * p):.4f}")   # -> 0.0042

# Multinomial: 12 clientes entre 3 planes con probabilidades 0,5 / 0,3 / 0,2
print(f"P(6, 4, 2) = {stats.multinomial.pmf([6, 4, 2], 12, [0.5, 0.3, 0.2]):.4f}")  # -> 0.0702
