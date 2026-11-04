#!/usr/bin/env python
"""P17 · Verificación de la ingesta de OpenF1.

    python verificar.py
"""

import csv
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent
DATOS = RAIZ / "data"
fallos, pasos = [], 0


def comprobar(condicion, mensaje):
    global pasos
    pasos += 1
    print(("  ok    " if condicion else "  FALLA ") + mensaje)
    if not condicion:
        fallos.append(mensaje)


def main():
    csvs = DATOS / "vueltas.csv"
    comprobar(csvs.exists(), "existe data/vueltas.csv")
    if not csvs.exists():
        return terminar()

    with csvs.open(encoding="utf-8") as fichero:
        filas = list(csv.DictReader(fichero))

    comprobar(len(filas) > 2000, f"hay más de 2.000 vueltas: {len(filas)}")
    sesiones = {f["sesion"] for f in filas}
    comprobar(len(sesiones) == 3, f"hay tres sesiones distintas: {len(sesiones)}")
    pilotos = {(f["sesion"], f["piloto"]) for f in filas}
    comprobar(len(pilotos) >= 55, f"hay al menos 55 pares sesión-piloto: {len(pilotos)}")

    claves = [(f["sesion"], f["piloto"], f["vuelta"]) for f in filas]
    comprobar(len(claves) == len(set(claves)), "no hay duplicados por sesión, piloto y vuelta")

    validas = [f for f in filas if f["duracion"]]
    comprobar(len(validas) > 0.85 * len(filas), f"al menos el 85 % tiene duración: {len(validas)} de {len(filas)}")
    comprobar(all(float(f["duracion"]) > 30 for f in validas), "todas las duraciones son mayores de 30 s")

    crudos = list((DATOS / "raw").glob("*.json"))
    comprobar(len(crudos) >= 5, f"el bruto está guardado: {len(crudos)} ficheros")

    print("\n  vueltas por sesión:")
    for sesion in sorted(sesiones):
        n = sum(1 for f in filas if f["sesion"] == sesion)
        circuito = next(f["circuito"] for f in filas if f["sesion"] == sesion)
        print(f"    {circuito:12s} {n:5d} vueltas")
    return terminar()


def terminar():
    print(f"\n{'P17 CORRECTO' if not fallos else 'HAY ' + str(len(fallos)) + ' FALLO(S)'}: {pasos} pasan, {len(fallos)} fallan.")
    return 0 if not fallos else 1


if __name__ == "__main__":
    sys.exit(main())
