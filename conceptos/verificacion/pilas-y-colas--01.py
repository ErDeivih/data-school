# Una pila resuelve el equilibrio de parentesis en una sola pasada.
def equilibrado(texto):
    parejas = {")": "(", "]": "[", "}": "{"}
    pila = []
    for c in texto:
        if c in "([{":
            pila.append(c)                       # apilar la apertura
        elif c in parejas:
            if not pila or pila.pop() != parejas[c]:
                return False                     # cierre sin apertura o mal emparejado
    return not pila                              # si queda algo, hay aperturas sin cerrar

print(equilibrado("{[()]}"))   # -> True
print(equilibrado("([)]"))     # -> False
print(equilibrado("((("))      # -> False
print(equilibrado(""))         # -> True
