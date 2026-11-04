import numpy as np

precios = np.array([100.0, 105.0, 99.0, 104.0])
log_ret = np.diff(np.log(precios))         # ln(P_t) - ln(P_t-1): se suman en el tiempo
simple = np.diff(precios) / precios[:-1]   # (P_t - P_t-1) / P_t-1: se multiplican

print(f"log del periodo 1  {log_ret[0]:+.6f}")       # -> +0.048790
print(f"log del periodo 2  {log_ret[1]:+.6f}")       # -> -0.058841
print(f"log del periodo 3  {log_ret[2]:+.6f}")       # -> +0.049271
print(f"suma de los logs   {log_ret.sum():+.6f}")    # -> +0.039221
print(f"ln(104/100)        {np.log(precios[-1] / precios[0]):+.6f}")  # -> +0.039221
print(f"suma de simples    {simple.sum():+.6f}")     # -> +0.043362
