#!/usr/bin/env python
"""PF-01 · Ingesta reproducible de un indicador público del Banco Mundial.

Descarga, guarda el bruto y normaliza a una tabla larga. Sin claves, sin dependencias
externas y con el mismo resultado en dos ejecuciones.

    python ingerir.py            # descarga y escribe data/
    python verificar.py          # comprueba el resultado
"""

import csv
import json
import pathlib
import time
import urllib.error
import urllib.request
from datetime import date

RAIZ = pathlib.Path(__file__).resolve().parent
DATOS = RAIZ / "data"
CRUDO = DATOS / "raw"

# Países y años: pequeño a propósito. Un pipeline que no se puede mirar entero no se depura.
PAISES = ["ESP", "FRA", "DEU", "ITA", "PRT"]
DESDE, HASTA = 2000, 2023
INDICADORES = {
    "SP.POP.TOTL": "poblacion",
    "NY.GDP.PCAP.CD": "pib_per_capita_usd",
}
BASE = "https://api.worldbank.org/v2/country/{paises}/indicator/{indicador}"
CABECERAS = {"User-Agent": "tramario-pf01/1.0 (proyecto de aprendizaje)"}


def descargar(url, intentos=3, espera=3):
    """GET con reintentos y espera creciente. Devuelve (bytes, fecha de descarga)."""
    ultimo = None
    for n in range(1, intentos + 1):
        try:
            peticion = urllib.request.Request(url, headers=CABECERAS)
            with urllib.request.urlopen(peticion, timeout=90) as respuesta:
                return respuesta.read(), date.today().isoformat()
        except (urllib.error.URLError, TimeoutError) as error:
            ultimo = error
            if n < intentos:
                time.sleep(espera * n)
    raise RuntimeError(f"No se pudo descargar {url}: {ultimo}")


def main():
    CRUDO.mkdir(parents=True, exist_ok=True)
    filas = []
    for codigo, nombre in INDICADORES.items():
        url = BASE.format(paises=";".join(PAISES), indicador=codigo)
        url += f"?format=json&per_page=2000&date={DESDE}:{HASTA}"
        crudo, fecha = descargar(url)
        destino = CRUDO / f"{nombre}-{fecha}.json"
        destino.write_bytes(crudo)

        datos = json.loads(crudo)
        if not isinstance(datos, list) or len(datos) < 2 or datos[1] is None:
            raise RuntimeError(f"Respuesta inesperada para {codigo}: sin datos")

        for registro in datos[1]:
            valor = registro.get("value")
            filas.append(
                {
                    "indicador": nombre,
                    "pais": registro["countryiso3code"],
                    "anio": int(registro["date"]),
                    "valor": "" if valor is None else valor,
                    "descarga": fecha,
                }
            )
        print(f"  {nombre}: {len(datos[1])} registros -> {destino.name}")

    filas.sort(key=lambda f: (f["indicador"], f["pais"], f["anio"]))
    salida = DATOS / "poblacion.csv"
    with salida.open("w", encoding="utf-8", newline="") as fichero:
        escritor = csv.DictWriter(fichero, fieldnames=["indicador", "pais", "anio", "valor", "descarga"])
        escritor.writeheader()
        escritor.writerows(filas)

    nulos = sum(1 for f in filas if f["valor"] == "")
    print(f"\n  {len(filas)} filas -> {salida} ({nulos} sin valor)")


if __name__ == "__main__":
    main()
