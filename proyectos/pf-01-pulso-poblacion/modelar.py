#!/usr/bin/env python
"""PF-01 · Ejecuta los modelos y sus pruebas sin depender del adaptador de dbt.

El proyecto es un proyecto dbt de verdad (`dbt_project.yml`, `models/`, `schema.yml`). Como en este
equipo solo está instalado el adaptador de Postgres, aquí se ejecuta el mismo SQL con DuckDB:
se sustituyen los `{{ ref(...) }}` por el nombre de la tabla y se crean las vistas y tablas del
almacén. Con `dbt-duckdb` instalado, `dbt build` haría exactamente esto.

    python modelar.py
"""

import pathlib
import re
import sys

import duckdb

RAIZ = pathlib.Path(__file__).resolve().parent
ALMACEN = RAIZ / "data" / "almacen.duckdb"
MODELOS = [
    ("stg_poblacion", RAIZ / "models" / "staging" / "stg_poblacion.sql"),
    ("dim_pais", RAIZ / "models" / "marts" / "dim_pais.sql"),
    ("f_poblacion", RAIZ / "models" / "marts" / "f_poblacion.sql"),
]

fallos = []


def sql_de(ruta):
    texto = ruta.read_text(encoding="utf-8")
    # {{ ref('stg_poblacion') }} -> stg_poblacion
    return re.sub(r"\{\{\s*ref\('([^']+)'\)\s*\}\}", r"\1", texto)


def comprobar(condicion, mensaje):
    print(("  ok    " if condicion else "  FALLA ") + mensaje)
    if not condicion:
        fallos.append(mensaje)


def main():
    ALMACEN.parent.mkdir(parents=True, exist_ok=True)
    if ALMACEN.exists():
        ALMACEN.unlink()
    con = duckdb.connect(str(ALMACEN))

    for nombre, ruta in MODELOS:
        con.execute(f"create or replace table {nombre} as {sql_de(ruta)}")
        filas = con.execute(f"select count(*) from {nombre}").fetchone()[0]
        print(f"  modelo {nombre}: {filas} filas")

    # Pruebas del schema.yml, en SQL.
    comprobar(con.execute("select count(*) from stg_poblacion").fetchone()[0] == 240, "stg_poblacion tiene 240 filas")
    comprobar(con.execute("select count(*) from stg_poblacion where valor is null").fetchone()[0] == 0, "no hay valores nulos")
    comprobar(
        con.execute("select count(*) from (select pais_iso3 from dim_pais group by 1 having count(*) > 1)").fetchone()[0] == 0,
        "dim_pais es única por pais_iso3",
    )
    comprobar(con.execute("select count(*) from dim_pais").fetchone()[0] == 5, "dim_pais tiene cinco países")
    comprobar(
        con.execute(
            """select count(*) from f_poblacion f
               left join dim_pais d using (pais_iso3) where d.pais_iso3 is null"""
        ).fetchone()[0] == 0,
        "todas las filas del hecho tienen su país en la dimensión",
    )
    comprobar(
        con.execute("select count(*) from (select indicador, pais_iso3, anio from f_poblacion group by 1, 2, 3 having count(*) > 1)").fetchone()[0] == 0,
        "el hecho es único por indicador, país y año",
    )
    comprobar(
        con.execute("select count(distinct anio) from f_poblacion").fetchone()[0] == 24,
        "el hecho cubre 24 años",
    )

    resumen = con.execute(
        """select d.pais, f.anio, round(f.valor / 1e6, 2) as millones
           from f_poblacion f join dim_pais d using (pais_iso3)
           where f.indicador = 'poblacion' and f.anio in (2000, 2023)
           order by d.pais, f.anio"""
    ).fetchall()
    print("\n  población (millones):")
    for pais, anio, millones in resumen:
        print(f"    {pais:10s} {anio}  {millones:6.2f}")

    print(f"\n{'MODELO CORRECTO' if not fallos else 'HAY ' + str(len(fallos)) + ' FALLO(S)'}")
    return 0 if not fallos else 1


if __name__ == "__main__":
    sys.exit(main())
