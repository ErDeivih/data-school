llegadas = [(1, 0), (4, 4), (7, 6), (9, 3), (12, 11), (15, 2)]   # (llega, tiempo de evento)
R, ANCHO = 3, 5                                                 # margen y tamano de ventana
max_visto, abiertas, publicadas, tardios = -99, {}, {}, []

for llega, evento in llegadas:
    max_visto = max(max_visto, evento)          # la marca de agua nunca retrocede
    marca = max_visto - R
    inicio = int(evento // ANCHO) * ANCHO       # a que ventana pertenece el evento
    if inicio in publicadas:                    # su ventana ya se publico: llega tarde
        tardios.append((llega, evento))
    else:
        abiertas[inicio] = abiertas.get(inicio, 0) + 1
    for w in sorted(abiertas):                  # cierra lo que la marca de agua ya dejo atras
        if w + ANCHO <= marca:
            publicadas[w] = abiertas.pop(w)
    print(f"llega {llega:2d}  evento {evento:2d}  marca {marca:3d}  abiertas {sorted(abiertas)}")

print("publicadas:", {f"8:{w:02d}": c for w, c in sorted(publicadas.items())})
print("abiertas al final:", {f"8:{w:02d}": c for w, c in sorted(abiertas.items())})
print("tardios:", tardios)
# -> publicadas: {'8:00': 3}
# -> abiertas al final: {'8:05': 1, '8:10': 1}
# -> tardios: [(15, 2)]
