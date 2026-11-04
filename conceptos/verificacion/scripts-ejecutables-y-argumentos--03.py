import sys
from pathlib import Path

def resumen(entrada: Path, limite: int) -> int:
    """Devuelve el codigo de salida: 0 bien, 2 mal uso, 1 fallo del entorno."""
    if limite <= 0:
        print("--limite tiene que ser positivo", file=sys.stderr)
        return 2                        # lo he llamado mal: reintentar no arregla nada
    if not entrada.exists():
        print(f"no encuentro {entrada}", file=sys.stderr)
        return 1                        # puede ser transitorio: aqui si tiene sentido reintentar
    return 0

# La ruta se construye; no se escribe ninguna ruta absoluta de esta maquina.
ruta = Path("datos") / "ventas" / "2026-01.csv"
print("la ruta por partes:", ruta.parts)      # -> la ruta por partes: ('datos', 'ventas', '2026-01.csv')
print("solo el nombre:", ruta.name)           # -> solo el nombre: 2026-01.csv
print("sin extension:", ruta.stem)            # -> sin extension: 2026-01
print("cambiando la extension:", ruta.with_suffix(".parquet").name)
# -> cambiando la extension: 2026-01.parquet
print("codigo con limite 0:", resumen(ruta, 0))                    # -> codigo con limite 0: 2
print("codigo con un fichero que no existe:", resumen(ruta, 10))   # -> codigo con un fichero que no existe: 1
print("el planificador solo mira si es cero:", resumen(ruta, 10) != 0)
# -> el planificador solo mira si es cero: True
