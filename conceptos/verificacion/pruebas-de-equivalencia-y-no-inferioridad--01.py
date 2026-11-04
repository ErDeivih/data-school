import numpy as np
from scipy import stats

# Ensayo de bioequivalencia: 100 sujetos por grupo, diferencia observada 0,20, s combinada 1,5.
d, s, n1, n2, margen = 0.20, 1.5, 100, 100, 0.5
ee = s * np.sqrt(1.0 / n1 + 1.0 / n2)
gl = n1 + n2 - 2

t90 = stats.t.ppf(0.95, gl)                       # una cola al 5 % = dos colas al 90 %
print(f"EE {ee:.3f}  IC90 ({d - t90 * ee:+.3f}, {d + t90 * ee:+.3f})  dentro del margen: "
      f"{abs(d) + t90 * ee < margen}")
# -> EE 0.212  IC90 (-0.151, +0.551)  dentro del margen: False

p1 = stats.t.sf((d + margen) / ee, gl)            # el limite de abajo, -margen
p2 = stats.t.cdf((d - margen) / ee, gl)           # el limite de arriba, +margen
print(f"p TOST = max({p1:.5f}, {p2:.5f}) = {max(p1, p2):.5f}   se rechaza: {max(p1, p2) < 0.05}")
# -> p TOST = max(0.00057, 0.07943) = 0.07943   se rechaza: False

# El contraste clasico da otra cosa: no detecta diferencia... y tampoco demuestra igualdad.
print(f"p bilateral clasico {2 * stats.t.sf(abs(d) / ee, gl):.3f}")
# -> p bilateral clasico 0.347
