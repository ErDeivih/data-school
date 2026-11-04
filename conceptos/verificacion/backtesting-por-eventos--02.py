# Lo que el backtest vectorizado se inventa cuando da por hecho el llenado completo.
objetivo, ejecutado = 500, 350
precio_entrada, subida = 100.0, 0.02
hueco = objetivo - ejecutado

print(f"el modelo cree tener {objetivo} acciones y tiene {ejecutado}")
print(f"exposicion inexistente: {hueco} acciones")
print(f"beneficio imaginario con una subida del 2 %: {hueco * precio_entrada * subida:.0f} EUR")
# -> beneficio imaginario con una subida del 2 %: 300 EUR
print(f"sobre una cuenta de 10000 EUR es un {(hueco * precio_entrada * subida) / 10000:.1%}")
# -> sobre una cuenta de 10000 EUR es un 3.0%
