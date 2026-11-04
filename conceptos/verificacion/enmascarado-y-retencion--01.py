import hashlib
import hmac
from collections import Counter

clave = b"clave-secreta-de-ejemplo"

def token(texto):
    return hmac.new(clave, texto.encode(), hashlib.sha256).hexdigest()[:12]

print(token("12345678A"), token("12345678A"), token("87654321B"))  # -> a66759ad9738 a66759ad9738 259a6586c28e

filas = [("28", "Madrid"), ("28", "Madrid"), ("28", "Madrid"),
         ("41", "Sevilla"), ("41", "Sevilla"), ("08", "Barcelona")]
grupos = Counter(filas)
print(f"grupos {len(grupos)}")                       # -> grupos 3
print(f"k minimo {min(grupos.values())}")            # -> k minimo 1
print(f"filas unicas {sum(1 for v in grupos.values() if v == 1)}")  # -> filas unicas 1