# 1) Anotar no valida: las anotaciones no se comprueban al ejecutar.
def dobla(precio: float) -> float:
    return precio * 2

print("con un numero  :", dobla(2.5))
print("con una cadena :", dobla("25"))     # "25" + "25": ni 50 ni error, otra cosa

# Comprobacion real, en la frontera: aqui es donde debe fallar.
def dobla_validando(precio):
    if not isinstance(precio, (int, float)) or isinstance(precio, bool):
        raise TypeError(f"precio debe ser numerico, llego {type(precio).__name__}")
    return precio * 2

try:
    dobla_validando("25")
except TypeError as exc:
    print("falla en la puerta:", exc)
