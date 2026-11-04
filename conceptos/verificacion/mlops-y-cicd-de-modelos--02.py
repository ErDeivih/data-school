# La huella del modelo: datos + hiperparametros + codigo identifican una ejecucion.
import hashlib, json

def huella(hash_datos, params, hash_codigo):
    carga = json.dumps({"datos": hash_datos, "params": params, "codigo": hash_codigo}, sort_keys=True)
    return hashlib.sha256(carga.encode()).hexdigest()[:16]

base = {"alpha": 1.0, "fit_intercept": True}
print("huella alpha 1.0:", huella("a1b2", base, "c3d4"))                    # -> huella alpha 1.0: ad1c8b5578dcdc98
print("huella alpha 1.1:", huella("a1b2", {**base, "alpha": 1.1}, "c3d4"))  # -> huella alpha 1.1: befc8d3137384312
