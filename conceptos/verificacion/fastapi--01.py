from pydantic import BaseModel, Field, ValidationError, field_validator

class AltaUsuario(BaseModel):
    email: str
    edad: int = Field(ge=18, le=120)      # cotas incluidas: 18 y 120 pasan, 17 y 121 no

    @field_validator("email")             # se ejecuta al validar ese campo, no al leer la clase
    @classmethod                          # Pydantic v2 exige este decorador DEBAJO del validador
    def normalizar(cls, v: str) -> str:
        return v.strip().lower()           # normaliza antes de guardar: sin espacios y en minusculas

print(AltaUsuario(email="  Ana@Ejemplo.COM ", edad=30))   # -> email='ana@ejemplo.com' edad=30

# Lo que el usuario manda como texto y FastAPI convierte a int: si no puede, responde 422.
try:
    edad = int("treinta")
except ValueError as exc:
    print("422 Unprocessable Entity:", exc)               # -> 422 Unprocessable Entity: invalid literal for int() with base 10: 'treinta'

try:
    AltaUsuario(email="ana@ejemplo.com", edad=15)
except ValidationError as exc:            # hereda de ValueError: capturarlo por su nombre lo distingue
    print("422:", exc.errors()[0]["msg"])                 # -> 422: Input should be greater than or equal to 18
# errors() devuelve una lista con un fallo por campo; [0] es el primero, el de la edad
