import base64
import hashlib
import hmac
import json

CLAVE = b"secreto-de-firma"

def b64(datos: bytes) -> str:
    return base64.urlsafe_b64encode(datos).decode().rstrip("=")
    # base64url sin el relleno de "=": es el formato que exige un JWT; decode() pasa bytes a texto

def firmar(cabecera: dict, carga: dict) -> str:
    h = b64(json.dumps(cabecera, separators=(",", ":")).encode())
    c = b64(json.dumps(carga, separators=(",", ":")).encode())    # sin espacios: si cambian, cambia la firma
    firma = b64(hmac.new(CLAVE, f"{h}.{c}".encode(), hashlib.sha256).digest())
    # HMAC-SHA256 de "cabecera.carga" con la clave secreta; digest() devuelve los bytes
    return f"{h}.{c}.{firma}"

def verificar(token: str) -> bool:
    h, c, firma = token.split(".")                   # tres partes; si no son tres, el desempaquetado falla
    esperada = b64(hmac.new(CLAVE, f"{h}.{c}".encode(), hashlib.sha256).digest())
    return hmac.compare_digest(firma, esperada)      # comparacion en tiempo constante

token = firmar({"alg": "HS256", "typ": "JWT"}, {"sub": "42", "rol": "admin", "exp": 1900000000})
print("partes del token:", len(token.split(".")))    # -> 3 partes
print("firma valida:", verificar(token))             # -> True

# Nadie puede cambiar el rol sin la clave: la firma deja de cuadrar.
h, c, _ = token.split(".")
carga_falsa = b64(json.dumps({"sub": "42", "rol": "superadmin"}).encode())
print("token manipulado:", verificar(f"{h}.{carga_falsa}.{token.split('.')[2]}"))   # -> False
# la carga se lee y se reescribe sin ninguna clave (es texto); lo que no se puede es recalcular la firma
