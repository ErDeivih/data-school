import re
import unicodedata

def normalizar(nombre):
    """Recorta espacios, quita tildes y deja una mayuscula inicial por palabra."""
    limpio = re.sub(r"\s+", " ", nombre).strip()
    sin_tildes = "".join(c for c in unicodedata.normalize("NFD", limpio)
                         if unicodedata.category(c) != "Mn")
    return sin_tildes.title()

sucios = ["  juan   pérez ", "MARIA gomez", " marta  ruiz-", "luis"]
print([normalizar(s) for s in sucios])
# -> ['Juan Perez', 'Maria Gomez', 'Marta Ruiz-', 'Luis']

# fullmatch exige que el patron cubra TODA la cadena; search habria dejado pasar basura.
CORREO = re.compile(r"[^@\s]+@[^@\s]+\.[a-z]{2,}")
candidatos = ["ana@x.com", "ANA@X.COM", "ana@x", "no-es-un-email", "ana@x.com "]
print([(c.strip().lower(), bool(CORREO.fullmatch(c.strip().lower()))) for c in candidatos])
# -> [('ana@x.com', True), ('ana@x.com', True), ('ana@x', False), ('no-es-un-email', False), ('ana@x.com', True)]
