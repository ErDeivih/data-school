import numpy as np

DIM = 256

def posicion(pieza, dim=DIM):
    """Hash propio y determinista: el mismo numero en cada ejecucion y en cada maquina.
    El hash() de Python no sirve aqui porque cambia de un proceso a otro."""
    valor = 0
    for letra in pieza:
        valor = (valor * 31 + ord(letra)) % dim   # el modulo deja el resultado dentro del vector
    return valor

def embedding(texto):
    """Embedding disperso determinista: suma un 1 por palabra y por bigrama."""
    # .lower() borra las mayusculas: "El" y "el" acaban en el mismo vector
    palabras = texto.lower().split()
    # bigramas con guion bajo: "pagos tardios" -> "pagos_tardios", asi se conserva algo de orden
    piezas = list(palabras) + [a + "_" + b for a, b in zip(palabras, palabras[1:])]
    v = np.zeros(DIM)
    for p in piezas:
        v[posicion(p)] += 1.0            # dos palabras distintas pueden caer en la misma casilla
    return v

def similitud(a, b):
    # norm() es la raiz de la suma de cuadrados: el denominador del coseno
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    # si un vector es todo ceros la division daria nan, y nan contamina cualquier max()
    return float(a @ b / (na * nb)) if na and nb else 0.0

def trocear(texto, w, s):
    # el rango avanza de s en s: el tamano de cada trozo es w y el salto es s, no son lo mismo
    return [texto[i:i + w] for i in range(0, len(texto), s)]

doc = ("La factura se emite el dia 1. El plazo de pago es de 30 dias "
       "desde la fecha de emision. Los pagos tardios devengan un interes del 3,75 %.")
consulta = embedding("interes por pagos tardios")

for nombre, s in (("sin solape", 34), ("con solape", 24)):
    trozos = trocear(doc, 34, s)
    # max() recorre los trozos y se queda con el mas parecido: asi se simula el top-1
    mejor = max(similitud(consulta, embedding(t)) for t in trozos)
    print(f"{nombre:12s} fragmentos {len(trozos):>2}  mejor similitud {mejor:.3f}")
