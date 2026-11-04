# Detector de fraude: 1.000 operaciones, 20 fraudes reales, 30 alertas y 18 aciertos
vp, fp, fn, vn = 18, 12, 2, 968

exactitud = (vp + vn) / (vp + fp + fn + vn)
precision = vp / (vp + fp)
exhaustividad = vp / (vp + fn)
f1 = 2 * precision * exhaustividad / (precision + exhaustividad)
especificidad = vn / (vn + fp)
balanced = (exhaustividad + especificidad) / 2

print(f"exactitud     {exactitud:.4f}")      # -> 0.9860
print(f"precision     {precision:.4f}")      # -> 0.6000
print(f"exhaustividad {exhaustividad:.4f}")  # -> 0.9000
print(f"F1            {f1:.4f}")             # -> 0.7200
print(f"balanced acc  {balanced:.4f}")       # -> 0.9439
