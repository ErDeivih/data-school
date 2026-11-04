import gzip, json

# 3.000 eventos con las mismas claves: en JSON la clave se repite en cada linea
eventos = [{"id": i, "ciudad": ["Madrid", "Barcelona", "Sevilla"][i % 3],
            "importe": round(10.0 + (i % 7), 2)} for i in range(3000)]

jsonl = "\n".join(json.dumps(e, ensure_ascii=False) for e in eventos).encode()
# Misma informacion en columnas: cada valor junto a los de su tipo
columnar = json.dumps({
    "id": [e["id"] for e in eventos],
    "ciudad": [e["ciudad"] for e in eventos],
    "importe": [e["importe"] for e in eventos],
}).encode()

print("bytes en JSON por lineas:", len(jsonl))     # -> bytes en JSON por lineas: 152889
print("bytes en columnar:", len(columnar))         # -> bytes en columnar: 68923
print("columnar mas pequeno:", len(columnar) < len(jsonl))   # -> columnar mas pequeno: True
print("gzip baja de la mitad:", len(gzip.compress(jsonl)) < len(jsonl) // 2)  # -> gzip baja de la mitad: True
