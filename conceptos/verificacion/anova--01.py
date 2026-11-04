import numpy as np
from scipy import stats

a = np.array([12, 14, 13, 15, 16])
b = np.array([10, 11, 12,  9, 13])
c = np.array([14, 16, 15, 13, 17])
grupos = [a, b, c]
todos = np.concatenate(grupos)

gl_entre, gl_dentro = len(grupos) - 1, todos.size - len(grupos)
ss_entre = sum(g.size * (g.mean() - todos.mean())**2 for g in grupos)
ss_dentro = sum(((g - g.mean())**2).sum() for g in grupos)

print(f"SS entre {ss_entre:.2f}  SS dentro {ss_dentro:.2f}")
# -> SS entre 43.33  SS dentro 30.00
print(f"F {ss_entre / gl_entre / (ss_dentro / gl_dentro):.3f}  "
      f"p {1 - stats.f.cdf(ss_entre / gl_entre / (ss_dentro / gl_dentro), gl_entre, gl_dentro):.4f}")
# -> F 8.667  p 0.0047
print(f"eta2 {ss_entre / (ss_entre + ss_dentro):.3f}")
# -> eta2 0.591
