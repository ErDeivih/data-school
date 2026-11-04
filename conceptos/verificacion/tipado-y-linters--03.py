# La frontera del pipeline: validar y convertir en la puerta, no al final.
from pydantic import BaseModel, Field, ValidationError

class Cliente(BaseModel):
    id: int = Field(ge=1)
    nombre: str
    saldo: float = Field(ge=0)
    activo: bool = True

crudo = {"id": 7, "nombre": "Ana", "saldo": "12.50", "activo": "true"}
c = Cliente(**crudo)
print("saldo convertido:", c.saldo, "activo:", c.activo)

malo = {"id": 7, "nombre": "Ana", "saldo": "doce"}
try:
    Cliente(**malo)
except ValidationError as exc:
    print("la puerta rechaza el lote:", exc.error_count(), "error")
    print(exc.errors()[0]["loc"], exc.errors()[0]["type"])
