import numpy as np

# La media miente con cola a la derecha; los percentiles aguantan.
ms = np.array([42, 48, 51, 55, 61, 66, 70, 74, 81, 95, 110, 140, 190, 320, 900], dtype=float)

print(f"media  {ms.mean():.1f}")
print(f"p50    {np.percentile(ms, 50):.0f}")
print(f"p95    {np.percentile(ms, 95):.0f}")
print("mediciones por debajo de la media:", int((ms < ms.mean()).sum()), "de", ms.size)
