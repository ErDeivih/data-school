import numpy as np

# Naive Bayes multinomial desde cero sobre conteos escritos a mano.
# Filas: 4 correos de spam y 2 de no spam. Columnas: "gratis", "premio".
conteos = {"spam": np.array([3.0, 2.0]), "no spam": np.array([0.0, 1.0])}
n_docs = {"spam": 4.0, "no spam": 2.0}
alpha, V = 1.0, 2   # suavizado de Laplace, vocabulario de 2 palabras

# Suavizado de Laplace: (n_j + alpha) / (n + alpha * V). Se hace de una vez para
# las dos palabras porque conteos[c] es un array; alpha y V son escalares.
log_verosimilitud = {
    c: np.log((conteos[c] + alpha) / (n_docs[c] + alpha * V)) for c in conteos
}
log_previa = {c: np.log(n_docs[c] / 6.0) for c in conteos}

# Correo nuevo: aparece "gratis" (2 veces) y no aparece "premio".
x = np.array([2.0, 0.0])
for c in conteos:
    # x tiene un 0 en las palabras ausentes, asi que no restan nada: es la
    # diferencia con BernoulliNB, que si penaliza las ausencias.
    puntuacion = log_previa[c] + float((x * log_verosimilitud[c]).sum())
    print(f"{c:<8} log P(clase) {log_previa[c]:+.3f}  puntuacion total {puntuacion:+.3f}")
# -> spam     log P(clase) -0.405  puntuacion total -1.216
# -> no spam  log P(clase) -1.099  puntuacion total -3.871

print("prediccion:", max(conteos, key=lambda c: (x * log_verosimilitud[c]).sum() + log_previa[c]))
# -> spam
