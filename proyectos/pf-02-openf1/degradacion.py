#!/usr/bin/env python
"""P17 · Degradación por compuesto: cruza stints con vueltas.

Para cada piloto y cada stint calcula la mediana de sus vueltas y la pendiente en segundos por
vuelta. Una pendiente alta significa que el neumático se degrada rápido en ese compuesto.

    python degradacion.py
"""

import csv
import json
import pathlib
import statistics
import urllib.request
from collections import defaultdict

RAIZ = pathlib.Path(__file__).resolve().parent
DATOS = RAIZ / "data"
BASE = "https://api.openf1.org/v1"
CABECERAS = {"User-Agent": "tramario-p17/1.0"}


def descargar(ruta):
    with urllib.request.urlopen(urllib.request.Request(BASE + "/" + ruta, headers=CABECERAS), timeout=90) as r:
        return json.loads(r.read())


def pendiente(puntos):
    """Mínimos cuadrados a mano: segundos por vuelta."""
    n = len(puntos)
    if n < 3:
        return None
    sx = sum(x for x, _ in puntos)
    sy = sum(y for _, y in puntos)
    sxy = sum(x * y for x, y in puntos)
    sxx = sum(x * x for x, _ in puntos)
    denominador = n * sxx - sx * sx
    if denominador == 0:
        return None
    return (n * sxy - sx * sy) / denominador


def main():
    with (DATOS / "vueltas.csv").open(encoding="utf-8") as fichero:
        vueltas = list(csv.DictReader(fichero))

    por_sesion = defaultdict(list)
    for v in vueltas:
        if v["duracion"]:
            por_sesion[v["sesion"]].append(v)

    filas = []
    for sesion, lista in por_sesion.items():
        circuito = lista[0]["circuito"]
        stints = descargar(f"stints?session_key={sesion}")
        (DATOS / "raw").mkdir(exist_ok=True)
        (DATOS / "raw" / f"stints-{sesion}.json").write_text(json.dumps(stints), encoding="utf-8")
        for stint in stints:
            piloto = str(stint.get("driver_number"))
            inicio, fin = stint.get("lap_start"), stint.get("lap_end")
            compuesto = (stint.get("compound") or "").upper()
            propias = [
                v for v in lista
                if v["piloto"] == piloto and inicio <= int(v["vuelta"]) <= fin and float(v["duracion"]) > 0
            ]
            if len(propias) < 3:
                continue
            tiempos = [float(v["duracion"]) for v in propias]
            x = list(range(len(tiempos)))
            filas.append(
                {
                    "sesion": sesion,
                    "circuito": circuito,
                    "piloto": piloto,
                    "stint": stint.get("stint_number"),
                    "compuesto": compuesto,
                    "vueltas": len(tiempos),
                    "mediana": round(statistics.median(tiempos), 3),
                    "pendiente": None if pendiente(list(zip(x, tiempos))) is None else round(pendiente(list(zip(x, tiempos))), 4),
                }
            )

    filas = [f for f in filas if f["pendiente"] is not None]
    filas.sort(key=lambda f: (f["circuito"], f["piloto"], f["stint"] or 0))
    salida = DATOS / "degradacion.csv"
    with salida.open("w", encoding="utf-8", newline="") as fichero:
        escritor = csv.DictWriter(fichero, fieldnames=list(filas[0].keys()))
        escritor.writeheader()
        escritor.writerows(filas)

    print(f"  {len(filas)} stints -> {salida}")
    resumen = defaultdict(list)
    for f in filas:
        resumen[f["compuesto"]].append(f["pendiente"])
    for compuesto, valores in sorted(resumen.items()):
        print(f"  {compuesto:8s} {len(valores):3d} stints  pendiente mediana {statistics.median(valores):+.4f} s/vuelta")


if __name__ == "__main__":
    main()
