# Elegir que fragmentos entran en la ventana: los mejor puntuados que quepan en el presupuesto.
fragmentos = [
    ("doc3#12", 950, 0.89),
    ("doc1#04", 400, 0.81),
    ("doc7#01", 1200, 0.77),
    ("doc2#09", 300, 0.74),
    ("doc5#03", 600, 0.70),
]
presupuesto = 2000          # tokens disponibles para el contexto recuperado

elegidos, usado = [], 0     # dos variables de golpe: la lista de elegidos y el contador de tokens
for nombre, tokens, score in sorted(fragmentos, key=lambda f: -f[2]):   # el menos delante ordena de mayor a menor
    if usado + tokens <= presupuesto:    # cabe entero: no se parte un fragmento
        elegidos.append(nombre)
        usado += tokens                  # se acumula para la siguiente decision

print("elegidos:", ", ".join(elegidos))          # -> doc3#12, doc1#04, doc2#09
print(f"tokens usados {usado} de {presupuesto}  descartados {len(fragmentos) - len(elegidos)}")
# -> 1650 de 2000  descartados 2
