import inspect
import pandas as pd

# La ayuda vive dentro del paquete instalado: es la de TU version y no necesita conexion.
firma = inspect.signature(pd.DataFrame.merge)
print("parametros  :", [p for p in firma.parameters if p != "self"])
print("por defecto :", firma.parameters["how"].default)
print("obligatorios:", [p.name for p in firma.parameters.values()
                        if p.name != "self" and p.default is inspect.Parameter.empty])
print("resumen     :", inspect.getdoc(pd.DataFrame.merge).splitlines()[0])

# No todo tiene firma inspeccionable: en las funciones escritas en C, la firma suele estar
# escrita a mano en la primera linea de la docstring.
try:
    inspect.signature(dict.update)
except ValueError as error:
    print("dict.update :", type(error).__name__)
    print("docstring   :", inspect.getdoc(dict.update).splitlines()[0])
