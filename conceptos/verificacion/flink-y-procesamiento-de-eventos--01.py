# Watermark con retraso fijo: cuántos eventos llegan tarde y cuáles
eventos = [(1, 100), (2, 103), (3, 105), (4, 101), (5, 106), (6, 104), (7, 102)]
retraso = 2

maximo = 0
procesados = 0
tardios = []
for i, t in eventos:
    maximo = max(maximo, t)
    marca = maximo - retraso
    if t < marca:
        tardios.append(i)
    else:
        procesados += 1

print(f"procesados {procesados}")        # -> procesados 5
print(f"tardios {len(tardios)}")          # -> tardios 2
print(f"ids tardios {tardios}")           # -> ids tardios [4, 7]
print(f"marca final {maximo - retraso}")  # -> marca final 104