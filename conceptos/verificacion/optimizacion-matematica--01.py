import numpy as np
from scipy.optimize import linprog

# max 2x + 3y  ->  min -2x - 3y   (linprog siempre minimiza)
# x + y <= 4,  x + 3y <= 6,  x >= 0,  y >= 0
res = linprog([-2, -3], A_ub=[[1, 1], [1, 3]], b_ub=[4, 6],
              bounds=[(0, None), (0, None)], method="highs")

print("x, y =", np.round(res.x, 4))       # -> [3. 1.]
print("objetivo =", round(-res.fun, 4))   # -> 9.0
