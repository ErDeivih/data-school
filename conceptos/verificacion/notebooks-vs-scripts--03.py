# Por que un notebook con salidas ensucia el control de versiones:
# las imagenes van dentro del JSON, en base64.
import json

def peso_aproximado(celdas_con_salida: int, kb_por_grafico: int = 120) -> int:
    """Kilobytes que ocupan las salidas guardadas de un notebook."""
    return celdas_con_salida * kb_por_grafico

print("10 graficos guardados:", peso_aproximado(10), "KB")
print("con 5 graficos:", peso_aproximado(5), "KB")
print("y cada reejecucion los reescribe enteros: True")

# La solucion no es borrar el notebook: es ejecutar sin guardar salidas
# (jupyter nbconvert --to notebook --execute) o versionar solo el .py generado.
