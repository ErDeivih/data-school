# Cuanto ocupa la dimension plana frente a la partida, con 2000 productos y 40 familias
import json

FAMILIAS = [f"familia-{i:02d}" for i in range(40)]

estrella = [{"producto_id": i, "nombre": f"producto-{i:04d}", "familia": FAMILIAS[i % 40]}
            for i in range(2000)]
copo = ([{"producto_id": i, "nombre": f"producto-{i:04d}", "familia_id": i % 40}
         for i in range(2000)]
        + [{"familia_id": i, "nombre": FAMILIAS[i]} for i in range(40)])

bytes_estrella = len(json.dumps(estrella, separators=(",", ":")).encode())
bytes_copo = len(json.dumps(copo, separators=(",", ":")).encode())

print("dimension plana (estrella):", bytes_estrella, "bytes")   # -> 136891 bytes
print("dimension partida (copo)  :", bytes_copo, "bytes")       # -> 123981 bytes
print("el copo ahorra            :", bytes_estrella - bytes_copo, "bytes")   # -> 12910 bytes
