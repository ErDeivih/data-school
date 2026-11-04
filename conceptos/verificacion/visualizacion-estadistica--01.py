import numpy as np
import matplotlib.pyplot as plt

# Boxplot sin Seaborn: mismos cuartiles, mismos bigotes, todo explicito.
ms = np.array([42, 48, 51, 55, 61, 66, 70, 74, 81, 95, 110, 140, 190, 320, 900], dtype=float)

q1, mediana, q3 = np.percentile(ms, [25, 50, 75])
iqr = q3 - q1
bigote = q3 + 1.5 * iqr
atipicos = ms[ms > bigote]

fig, ax = plt.subplots()
ax.boxplot(ms, orientation="horizontal")
ax.set_xlabel("ms")
print("Q1, mediana, Q3:", q1, mediana, q3)
print("IQR:", iqr)
print("limite del bigote:", bigote)
print("atipicos:", atipicos.tolist())
print("media:", round(ms.mean(), 1))
