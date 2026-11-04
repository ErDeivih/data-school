# El limite que hace probable el dominio: dos adaptadores, el mismo caso de uso, cero base de datos
from typing import Protocol

class Reloj(Protocol):
    def hoy(self) -> str: ...

class RepositorioSuscripciones(Protocol):
    def buscar(self, cliente: str) -> dict: ...

class ServicioDeCobro:
    def __init__(self, repositorio: RepositorioSuscripciones, reloj: Reloj):
        self.repositorio = repositorio        # el dominio no sabe de donde vienen los datos
        self.reloj = reloj

    def a_cobrar(self, cliente: str) -> bool:
        suscripcion = self.repositorio.buscar(cliente)
        return suscripcion["activa"] and suscripcion["vence"] <= self.reloj.hoy()

class RepositorioDePrueba:                     # adaptador en memoria, para los tests
    def __init__(self, datos):
        self.datos = datos

    def buscar(self, cliente):
        return self.datos[cliente]

class RelojFijo:
    def __init__(self, fecha):
        self.fecha = fecha

    def hoy(self):
        return self.fecha

datos = {"ana": {"activa": True, "vence": "2026-10-01"},
         "luis": {"activa": False, "vence": "2026-01-01"}}
servicio = ServicioDeCobro(RepositorioDePrueba(datos), RelojFijo("2026-10-15"))
print("ana:", servicio.a_cobrar("ana"), " luis:", servicio.a_cobrar("luis"))
# -> ana: True  luis: False
