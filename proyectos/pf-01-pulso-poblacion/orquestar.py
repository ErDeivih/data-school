#!/usr/bin/env python
"""PF-01 · Orquestación mínima: los tres pasos en orden, con log y código de salida.

No es Dagster ni Airflow: es el mismo contrato (orden, reintento, log, fallo ruidoso) en 60 líneas,
para que la diferencia entre «un script» y «un pipeline» se vea en el código y no en la teoría.

    python orquestar.py
"""

import pathlib
import subprocess
import sys
from datetime import datetime

RAIZ = pathlib.Path(__file__).resolve().parent
LOG = RAIZ / "data" / "orquestacion.log"


def apuntar(texto):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fichero:
        fichero.write(f"[{datetime.now().isoformat(timespec='seconds')}] {texto}\n")


def paso(nombre, comando, comprobacion, intentos=2):
    for intento in range(1, intentos + 1):
        apuntar(f"empieza {nombre} (intento {intento})")
        resultado = subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)
        if resultado.returncode == 0 and comprobacion():
            apuntar(f"termina {nombre}")
            print(f"  ok    {nombre}")
            return True
        apuntar(f"falla {nombre}: {resultado.stderr.strip()[:200]}")
        print(f"  fallo {nombre} (intento {intento})")
    return False


def main():
    pasos = [
        ("ingesta", [sys.executable, "ingerir.py"], lambda: (RAIZ / "data" / "poblacion.csv").exists()),
        ("modelo", [sys.executable, "modelar.py"], lambda: (RAIZ / "data" / "almacen.duckdb").exists()),
        ("panel", [sys.executable, "panel.py"], lambda: (RAIZ / "panel.html").exists()),
        ("verificacion", [sys.executable, "verificar.py"], lambda: True),
    ]
    for nombre, comando, comprobacion in pasos:
        if not paso(nombre, comando, comprobacion):
            apuntar("se corta la ejecucion")
            print("\nORQUESTACION FALLIDA: revisa data/orquestacion.log")
            return 1
    apuntar("ejecucion completa")
    print("\nORQUESTACION CORRECTA: ingesta -> modelo -> panel -> verificacion")
    return 0


if __name__ == "__main__":
    sys.exit(main())
