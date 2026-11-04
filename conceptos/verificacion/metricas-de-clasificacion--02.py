# El clasificador trivial que dice "no" a todo: exactitud alta y utilidad nula.
n, fraudes = 1000, 20
vp, fp, fn, vn = 0, 0, fraudes, n - fraudes

print(f"exactitud     {(vp + vn) / n:.4f}")   # -> 0.9800
print(f"exhaustividad {vp / (vp + fn):.4f}")   # -> 0.0000
print("alertas lanzadas:", vp + fp)           # -> 0
