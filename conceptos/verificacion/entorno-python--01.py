import re

requisitos = """numpy==2.5.2
pandas==3.0.6
scipy>=1.18,<2.0
scikit-learn==1.5.2
requests
"""

lineas = [l.strip() for l in requisitos.strip().splitlines()]
fijadas = [l for l in lineas if "==" in l]
rangos = [l for l in lineas if "==" not in l and re.search(r"[<>~]=", l)]
sueltas = [l for l in lineas if l not in fijadas and l not in rangos]

print(f"lineas en el fichero  {len(lineas)}")   # -> 5
print(f"con version exacta    {len(fijadas)}")  # -> 3
print(f"con rango             {len(rangos)}")   # -> 1
print(f"sin restriccion       {len(sueltas)}")  # -> 1
