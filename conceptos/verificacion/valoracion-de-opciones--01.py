import math
from scipy.stats import norm

S0, K, r, sigma, T = 100.0, 100.0, 0.03, 0.25, 1.0

d1 = (math.log(S0 / K) + (r + sigma ** 2 / 2) * T) / (sigma * math.sqrt(T))
d2 = d1 - sigma * math.sqrt(T)
call = S0 * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
put = call - S0 + K * math.exp(-r * T)

print(f"d1 {d1:.4f} d2 {d2:.4f}")                      # -> d1 0.2450 d2 -0.0050
print(f"call {call:.2f} put {put:.2f}")                # -> call 11.35 put 8.39
print(f"paridad {call - put - S0 + K * math.exp(-r * T):+.10f}")  # -> paridad +0.0000000000