# La frontera, medida: cuantos fragmentos contienen la frase clave entera.
doc = ("La factura se emite el dia 1. El plazo de pago es de 30 dias "
       "desde la fecha de emision. Los pagos tardios devengan un interes del 3,75 %.")
frase_clave = "pagos tardios"

def trocear(texto, w, s):
    return [texto[i:i + w] for i in range(0, len(texto), s)]

def integros(trozos, frase):
    # sum() sobre booleanos cuenta los True: asi se cuenta en cuantos trozos aparece la frase
    return sum(frase in t for t in trozos)

print("documento con", len(doc), "caracteres")
for s in (34, 24):
    trozos = trocear(doc, 34, s)
    print(f"salto {s}: {len(trozos)} fragmentos, "
          f"{integros(trozos, frase_clave)} conservan la frase entera")
# salto 24 (solapamiento 10) recupera la frase; salto 34 la parte entre dos fragmentos
