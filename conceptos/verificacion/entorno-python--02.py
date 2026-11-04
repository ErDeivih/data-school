import hashlib

requisitos = "numpy==2.5.2\npandas==3.0.6\nscipy>=1.18,<2.0\nscikit-learn==1.5.2\nrequests\n"
# El mismo fichero con un solo caracter cambiado en el rango de scipy
cambiado = requisitos.replace(">=1.18", ">=1.19")

def huella(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()

print(f"huella original       {huella(requisitos)[:16]}")   # -> 4be22d82cce0b8c4
print(f"huella con un cambio  {huella(cambiado)[:16]}")     # -> 0c46a8447de41818
print(f"coinciden             {huella(requisitos) == huella(cambiado)}")  # -> False
