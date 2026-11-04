# No hay que reejecutar el notebook para auditar el orden: basta leer los contadores.
import json

cuaderno = {
    "cells": [
        {"cell_type": "code", "execution_count": 2, "source": ["x = 1\n"]},
        {"cell_type": "markdown", "source": ["# Analisis\n"]},
        {"cell_type": "code", "execution_count": 1, "source": ["print(x)\n"]},
        {"cell_type": "code", "execution_count": None, "source": ["print('sin ejecutar')\n"]},
    ],
    "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3"}},
}

crudo = json.dumps(cuaderno)
codigo = [c for c in cuaderno["cells"] if c["cell_type"] == "code"]
sin_ejecutar = [c for c in codigo if c["execution_count"] is None]

print("celdas totales:", len(cuaderno["cells"]))
print("celdas de codigo:", len(codigo))
print("sin ejecutar:", len(sin_ejecutar))
print("kernel:", cuaderno["metadata"]["kernelspec"]["name"])
print("el kernel no viaja en el codigo, solo el nombre:", '"import"' in crudo)
