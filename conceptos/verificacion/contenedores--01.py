import hashlib

def huellas(lineas):
    """Cada capa depende de la anterior: cambiar una linea invalida las siguientes."""
    anterior, salida = "inicio", []
    for linea in lineas:
        # El hash encadena el contenido de la linea CON el de la capa anterior: por eso una
        # capa no se identifica sola, se identifica dentro de la cadena que la precede.
        anterior = hashlib.sha256((anterior + linea).encode()).hexdigest()[:6]
        salida.append(anterior)
    return salida

base = ["FROM python:3.12-slim",
        "COPY requirements.txt .",
        "RUN pip install -r requirements.txt",
        "COPY app.py ."]

# Cambia solo el codigo de la aplicacion
otro_codigo = base[:3] + ["COPY app.py .  # version nueva"]
# Cambian las dependencias: la capa del pip y todo lo que va detras
otras_dependencias = base[:2] + ["RUN pip install -r requirements.txt  # con numpy", base[3]]

# zip empareja capa con capa en orden y sum() cuenta las coincidencias: las reutilizadas.
reutilizadas_codigo = sum(a == b for a, b in zip(huellas(base), huellas(otro_codigo)))
reutilizadas_deps = sum(a == b for a, b in zip(huellas(base), huellas(otras_dependencias)))

print("al tocar solo el codigo se reutilizan:", reutilizadas_codigo, "de", len(base))   # -> 3 de 4
print("al tocar las dependencias se reutilizan:", reutilizadas_deps, "de", len(base))   # -> 2 de 4
