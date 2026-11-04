import hashlib, json

def huella(estado):
    # Resumen estable del estado: el mismo contenido da siempre la misma huella
    return hashlib.sha256(json.dumps(estado, sort_keys=True).encode()).hexdigest()[:12]

declarado = {"nodos": 3, "tipo": "standard-4", "autoscaling": True}
observado = {"nodos": 5, "tipo": "standard-4", "autoscaling": True}   # alguien toco la consola

campos = sorted(set(declarado) | set(observado))
deriva = [c for c in campos if declarado[c] != observado.get(c)]

print("huella declarada:", huella(declarado))        # -> 6fadfd3a9ebf
print("huella observada:", huella(observado))        # -> c0651201979b
print("campos con deriva:", deriva)                  # -> ['nodos']
print("coincide tras aplicar:", huella({**observado, "nodos": 3}) == huella(declarado))  # -> True
