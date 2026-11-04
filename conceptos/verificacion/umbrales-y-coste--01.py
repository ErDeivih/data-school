import numpy as np

# Doce alertas ordenadas por puntuacion. y = 1 si el caso era realmente un fraude.
y = np.array([1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0])
score = np.array([0.97, 0.91, 0.88, 0.72, 0.65, 0.61,
                  0.44, 0.39, 0.30, 0.25, 0.12, 0.04])

c_fp, c_fn = 3.0, 200.0   # bloquear una compra legitima / dejar pasar un fraude

for umbral in (0.95, 0.75, 0.50, 0.25, 0.00):
    pred = score >= umbral
    # Con arrays se usa & y no `and`; los parentesis de cada comparacion son obligatorios.
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    # :>2 y :>6.0f son anchos de campo: alinean a la derecha en 2 y 6 caracteres para que
    # las columnas de la salida queden a plomo. No redondean los calculos, solo el texto.
    print(f"umbral {umbral:.2f}  alertas {int(pred.sum()):>2}  "
          f"FP {fp:>2}  FN {fn:>2}  coste {c_fp * fp + c_fn * fn:>6.0f}")
