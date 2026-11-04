import hashlib

def construir(fuente, dependencias, momento):
    """El digest depende del codigo, de las dependencias y del entorno de construccion."""
    # El momento de la construccion entra en el hash: por eso reconstruir da otro digest.
    # [:12] es solo para que la salida se lea; un digest real son 64 caracteres.
    return hashlib.sha256(f"{fuente}:{dependencias}:{momento}".encode()).hexdigest()[:12]

codigo, deps = "app-v3", "numpy-2.1.0"
construido_en_ci = construir(codigo, deps, "2026-01-01T10:00")
reconstruido_en_prod = construir(codigo, deps, "2026-01-01T10:07")   # mismo codigo, otra hora

# Cadena de asignacion: las tres variables apuntan a la MISMA cadena, no a tres copias.
staging = produccion = construido_en_ci        # se promueve el mismo artefacto

print("digest construido una vez en CI:", construido_en_ci)
print("staging y produccion usan el mismo digest:", staging == produccion)                  # -> True
print("digest reconstruido siete minutos despues:", reconstruido_en_prod)
print("lo que se probo es lo que se despliega:", construido_en_ci == reconstruido_en_prod)  # -> False
