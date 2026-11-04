import json
import re

# Lista negra por NOMBRE de campo: lo que no se anuncia como sensible, no se protege.
SENSIBLES = re.compile(r"(password|passwd|secret|token|api[_-]?key|authorization)", re.I)
# re.I hace la busqueda insensible a mayusculas: "Password" y "PASSWORD" tambien entran.

registro = {
    "usuario": "ana",
    "password": "hunter2-que-no-se-ve",
    "tarjeta": "4111111111111111",
    "token_acceso": "eyJhbGciOiJIUzI1NiJ9",
}

# Comprension sobre los .items(): conserva las claves y sustituye solo el valor sensible.
limpio = {k: ("***" if SENSIBLES.search(k) else v) for k, v in registro.items()}
# sort_keys hace la linea reproducible: el mismo diccionario imprime siempre en el mismo orden.
linea = json.dumps(limpio, ensure_ascii=False, sort_keys=True)

print(linea)
print("la contrasena aparece en la linea:", "hunter2-que-no-se-ve" in linea)   # -> False
print("el token aparece en la linea:", "eyJhbGciOiJIUzI1NiJ9" in linea)        # -> False
# La tarjeta no lleva palabra clave en el nombre, asi que pasa el filtro entera.
print("la tarjeta aparece en la linea:", "4111111111111111" in linea)          # -> True
