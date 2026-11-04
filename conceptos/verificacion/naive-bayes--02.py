import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Corpus diminuto y escrito a mano: "informe" y "trimestral" solo salen en no spam.
textos = [
    "gratis premio gratis enhorabuena", "premio gratis reclama ahora",
    "gratis oferta premio gratis", "premio gratis dinero gratis",
    "informe adjunto trimestral", "adjunto el informe trimestral",
]
etiquetas = [1, 1, 1, 1, 0, 0]

vec = CountVectorizer()                     # aprende el vocabulario del corpus
X = vec.fit_transform(textos)               # matriz dispersa documentos x palabras
# transform (no fit_transform): usa el vocabulario ya aprendido. Una palabra que
# no estuviera en el corpus se ignoraria en silencio.
nuevo = vec.transform(["gratis informe"])   # mezcla de las dos clases

# Cuanto mayor es alpha, mas se suavizan las probabilidades extremas.
for alpha in (1e-9, 0.1, 1.0):
    m = MultinomialNB(alpha=alpha).fit(X, etiquetas)
    prob = m.predict_proba(nuevo)[0]
    print(f"alpha {alpha:<8g} P(spam) {prob[1]:.3f}  P(no spam) {prob[0]:.3f}  predice {int(m.predict(nuevo)[0])}")
# -> alpha 1e-09    P(spam) 0.573  P(no spam) 0.427  predice 1
# -> alpha 0.1      P(spam) 0.603  P(no spam) 0.397  predice 1
# -> alpha 1        P(spam) 0.703  P(no spam) 0.297  predice 1
