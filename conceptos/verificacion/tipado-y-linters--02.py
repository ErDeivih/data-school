from dataclasses import dataclass, field

# La dataclass declara la forma del dato y genera __init__ y __repr__.
# Lo que NO hace: validar tipos al construir.
@dataclass
class Pedido:
    id: int
    importe: float
    descuento: float = 0.0
    etiquetas: list[str] = field(default_factory=list)

    def total(self) -> float:
        return self.importe * (1 - self.descuento)

p = Pedido(id=7, importe=100.0, descuento=0.15)
print(p)
print("total:", p.total())

# Sin descuento, el valor por defecto es 0.0
print("total sin descuento:", Pedido(id=8, importe=50.0).total())

# Y aqui esta el peligro: la dataclass NO valida. Un importe en texto entra sin protestar.
raro = Pedido(id=9, importe="100.0")
print("acepta texto sin quejarse:", raro.importe)

# La conversion, cuando hace falta, es explicita:
print("convertido a numero:", float(raro.importe) + 1)
