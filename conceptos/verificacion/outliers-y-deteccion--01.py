import numpy as np

valores = np.array([8, 9, 10, 10, 11, 12, 12, 13, 14, 15, 16, 45], dtype=float)
q1, q3 = np.percentile(valores, [25, 75])
iqr = q3 - q1
mediana = np.median(valores)
mad = np.median(np.abs(valores - mediana))

print(f"Q1 {q1}  Q3 {q3}  IQR {iqr}")                        # -> Q1 10.0  Q3 14.25  IQR 4.25
print(f"valla superior {q3 + 1.5 * iqr}")                   # -> valla superior 20.625
print(f"MAD {mad}")                                         # -> MAD 2.0
print(f"z de 45 {(45 - valores.mean()) / valores.std(ddof=1):.3f}")          # -> z de 45 3.080
print(f"z modificado de 45 {0.6745 * (45 - mediana) / mad:.3f}")             # -> z modificado de 45 11.129
print(f"z modificado de 16 {0.6745 * (16 - mediana) / mad:.3f}")             # -> z modificado de 16 1.349
