# 1.000 eventos y 77 reintentos: qué pasa con y sin clave de idempotencia
ids = list(range(1000))
entregas = ids + [i for i in ids if i % 13 == 0]

vistos = set()
duplicados = 0
for i in entregas:
    if i in vistos:
        duplicados += 1
    else:
        vistos.add(i)

print(f"entregas {len(entregas)}")          # -> entregas 1077
print(f"unicos {len(vistos)}")               # -> unicos 1000
print(f"duplicados {duplicados}")            # -> duplicados 77
print(f"cobertura {len(vistos) / 1000:.1%}")  # -> cobertura 100.0%