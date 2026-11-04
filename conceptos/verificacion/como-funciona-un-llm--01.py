import numpy as np

logits = np.array([2.0, 1.0, 0.1])     # puntuaciones del ultimo token del vocabulario

def softmax(z, temperatura=1.0):
    z = z / temperatura              # T<1 separa los logits (menos dudas); T>1 los acerca
    e = np.exp(z - z.max())            # restar el maximo evita desbordar el exp
    return e / e.sum()                 # divide entre la suma: asi el vector suma 1

p1 = softmax(logits, 1.0)
p05 = softmax(logits, 0.5)

print("temperatura 1.0 ->", " ".join(f"{p:.3f}" for p in p1))     # -> 0.659 0.242 0.099
print("temperatura 0.5 ->", " ".join(f"{p:.3f}" for p in p05))    # -> 0.864 0.117 0.019

# Perplejidad de una frase de tres tokens: exp(entropia cruzada media)
probs = np.array([0.60, 0.50, 0.80])   # probabilidad que el modelo dio al token correcto
entropia = -np.log(probs).mean()       # -log de cada acierto y media de los tres
print(f"entropia cruzada {entropia:.4f}  perplejidad {np.exp(entropia):.2f}")   # -> 0.4757  1.61
