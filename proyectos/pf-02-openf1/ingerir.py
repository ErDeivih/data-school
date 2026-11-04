#!/usr/bin/env python
"""P17 · Ingesta real de OpenF1: de la API a una tabla que no se duplica.

Descarga tres carreras de 2024, guarda el bruto con su fecha y normaliza las vueltas a un CSV con
clave estable. Reejecutarlo no duplica: la clave es sesión, piloto y vuelta.

    python ingerir.py      # descarga y escribe data/
    python verificar.py    # comprueba forma, duplicados y cobertura
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
BASE = "https://api.openf1.org/v1"
CABECERAS = {"User-Agent": "tramario-p17/1.0 (proyecto de aprendizaje)"}
CARRERAS = 3


def descargar(ruta, intentos=3):
    url = f"{BASE}/{ruta}"
    ultimo = None
    for n in range(1, intentos + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=CABECERAS), timeout=90) as r:
                return json.loads(r.read())
        except (urllib.error.URLError, TimeoutError) as error:
            ultimo = error
            if n < intentos:
                time.sleep(2 * n)
    raise RuntimeError(f"No se pudo descargar {url}: {ultimo}")


def guardar(nombre, datos):
    CRUDO.mkdir(parents=True, exist_ok=True)
    destino = CRUDO / f"{nombre}-{date.today().isoformat()}.json"
    destino.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
    return destino


def main():
    sesiones = [s for s in descargar("sessions?year=2024&session_name=Race") if s.get("session_key")]
    sesiones.sort(key=lambda s: s.get("date_start") or "")
    elegidas = sesiones[:CARRERAS]
    guardar("sesiones", elegidas)
    print(f"  sesiones: {len(elegidas)} de {len(sesiones)} carreras de 2024")

    filas = []
    for sesion in elegidas:
        clave = sesion["session_key"]
        circuito = sesion.get("circuit_short_name") or sesion.get("location") or str(clave)
        pilotos = descargar(f"drivers?session_key={clave}")
        vueltas = descargar(f"laps?session_key={clave}")
        guardar(f"pilotos-{clave}", pilotos)
        guardar(f"vueltas-{clave}", vueltas)

        for v in vueltas:
            filas.append(
                {
                    "sesion": clave,
                    "circuito": circuito,
                    "piloto": v.get("driver_number"),
                    "vuelta": v.get("lap_number"),
                    "duracion": v.get("lap_duration"),
                    "s1": v.get("duration_sector_1"),
                    "s2": v.get("duration_sector_2"),
                    "s3": v.get("duration_sector_3"),
                    "salida_de_box": "1" if v.get("is_pit_out_lap") else "0",
                }
            )
        print(f"  {circuito}: {len(pilotos)} pilotos, {len(vueltas)} vueltas")

    # Clave de idempotencia: una vuelta de un piloto en una sesión. Se descarta lo repetido.
    recibidas = len(filas)
    unicas = {}
    for f in filas:
        unicas[(f["sesion"], f["piloto"], f["vuelta"])] = f
    filas = [unicas[k] for k in sorted(unicas, key=lambda k: (str(k[0]), k[1] or 0, k[2] or 0))]

    DATOS.mkdir(parents=True, exist_ok=True)
    salida = DATOS / "vueltas.csv"
    with salida.open("w", encoding="utf-8", newline="") as fichero:
        escritor = csv.DictWriter(fichero, fieldnames=list(filas[0].keys()))
        escritor.writeheader()
        escritor.writerows(filas)

    print(f"\n  {len(filas)} vueltas únicas -> {salida}")
    print(f"  recibidas {recibidas}, descartadas por clave repetida {recibidas - len(filas)}")


if __name__ == "__main__":
    main()
