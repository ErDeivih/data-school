import numpy as np

logits = np.array([5.0, 2.0, 0.5])      # la clase correcta, una confusion, una absurda


def softmax(z):
    e = np.exp(z - z.max())             # se resta el maximo por estabilidad numerica
    return e / e.sum()


for temperatura in (1, 2, 4):
    p = softmax(logits / temperatura)
    entropia = -(p * np.log(p)).sum()
    print(f"T={temperatura}  correcta={p[0]:.4f}  erronea={p[1]:.4f}"
          f"  absurda={p[2]:.4f}  entropia={entropia:.4f}")
# -> T=1  correcta=0.9426  erronea=0.0469  absurda=0.0105  entropia=0.2470
# -> T=2  correcta=0.7527  erronea=0.1680  absurda=0.0793  entropia=0.7145
# -> T=4  correcta=0.5565  erronea=0.2629  absurda=0.1807  entropia=0.9865
