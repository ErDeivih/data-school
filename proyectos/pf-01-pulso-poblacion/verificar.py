#!/usr/bin/env python
"""PF-01 · Verificación de la ingesta.

Comprueba que el CSV tiene la forma esperada y que el bruto está guardado. No mide calidad
del dato del Banco Mundial: mide que el pipeline hizo lo que dice.

    python verificar.py
"""

import csv
import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent
DATOS = RAIZ / "data"
ESPERADO_PAISES = {"ESP", "FRA", "DEU", "ITA", "PRT"}
ESPERADO_ANIOS = set(range(2000, 2024))
ESPERADO_INDICADORES = {"poblacion", "pib_per_capita_usd"}

fallos, pasos = [], 0


def comprobar(condicion, mensaje):
    global pasos
    pasos += 1
    if condicion:
        print(f"  ok    {mensaje}")
    else:
        fallos.append(mensaje)
        print(f"  FALLA {mensaje}")


def main():
    csvs = DATOS / "poblacion.csv"
    comprobar(csvs.exists(), "existe data/poblacion.csv")
    if not csvs.exists():
        return terminar()

    with csvs.open(encoding="utf-8") as fichero:
        filas = list(csv.DictReader(fichero))

    comprobar(len(filas) == 240, f"hay 240 filas (5 países x 24 años x 2 indicadores): {len(filas)}")
    comprobar(
        {f["pais"] for f in filas} == ESPERADO_PAISES,
        "los cinco países están",
    )
    comprobar({int(f["anio"]) for f in filas} == ESPERADO_ANIOS, "los 24 años están")
    comprobar({f["indicador"] for f in filas} == ESPERADO_INDICADORES, "los dos indicadores están")

    claves = [(f["indicador"], f["pais"], f["anio"]) for f in filas]
    comprobar(len(claves) == len(set(claves)), "no hay duplicados por indicador, país y año")
    comprobar(all(f["valor"] for f in filas), "no hay valores vacíos")
    comprobar(
        all(float(f["valor"]) > 0 for f in filas),
        "todos los valores son positivos (población y PIB per cápita)",
    )

    crudos = list((DATOS / "raw").glob("*.json"))
    comprobar(len(crudos) >= 2, f"el bruto está guardado: {len(crudos)} ficheros")
    for ruta in crudos[:2]:
        with ruta.open(encoding="utf-8") as fichero:
            datos = json.load(fichero)
        comprobar(isinstance(datos, list) and len(datos) >= 2, f"{ruta.name} conserva la respuesta original")

    return terminar()


def terminar():
    print(f"\n{'PF-01 CORRECTO' if not fallos else 'HAY ' + str(len(fallos)) + ' FALLO(S)'}: {pasos} pasan, {len(fallos)} fallan.")
    return 0 if not fallos else 1


if __name__ == "__main__":
    sys.exit(main())
