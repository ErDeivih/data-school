#!/usr/bin/env python
"""PF-01 · Panel de una sola página, sin servidor y sin dependencias.

Lee el almacén construido por modelar.py y escribe panel.html con dos gráficos y una tabla.
Se abre con doble clic: no necesita nada más.

    python panel.py
"""

import html
import pathlib

import duckdb

RAIZ = pathlib.Path(__file__).resolve().parent
ALMACEN = RAIZ / "data" / "almacen.duckdb"
SALIDA = RAIZ / "panel.html"

COLORES = {"2000": "#8a8f98", "2023": "#1d6f5c"}


def barras(datos, titulo, unidad, ancho=640):
    """Barras horizontales agrupadas: dos valores por país."""
    paises = [d[0] for d in datos]
    maximo = max(max(d[1], d[2]) for d in datos) or 1
    alto_fila = 44
    alto = 40 + alto_fila * len(paises)
    partes = [f'<svg viewBox="0 0 {ancho} {alto}" role="img" aria-label="{html.escape(titulo)}" class="grafico">']
    partes.append(f'<text x="0" y="16" class="titulo-grafico">{html.escape(titulo)} ({html.escape(unidad)})</text>')
    for i, (pais, v2000, v2023) in enumerate(datos):
        y = 34 + i * alto_fila
        partes.append(f'<text x="0" y="{y + 12}" class="etiqueta">{html.escape(pais)}</text>')
        for j, (anio, valor) in enumerate((("2000", v2000), ("2023", v2023))):
            largo = int((valor / maximo) * (ancho - 210))
            partes.append(
                f'<rect x="110" y="{y + j * 14}" width="{largo}" height="11" fill="{COLORES[anio]}" rx="2" />'
            )
            partes.append(
                f'<text x="{112 + largo}" y="{y + j * 14 + 10}" class="valor">{valor:,.0f}</text>'
            )
    partes.append("</svg>")
    return "\n".join(partes)


def main():
    con = duckdb.connect(str(ALMACEN), read_only=True)
    filas = con.execute(
        """select d.pais,
                  max(case when f.anio = 2000 then f.valor end) as v2000,
                  max(case when f.anio = 2023 then f.valor end) as v2023
           from f_poblacion f join dim_pais d using (pais_iso3)
           where f.indicador = ?
           group by d.pais order by v2023 desc"""
    , ["poblacion"]).fetchall()
    renta = con.execute(
        """select d.pais,
                  max(case when f.anio = 2000 then f.valor end) as v2000,
                  max(case when f.anio = 2023 then f.valor end) as v2023
           from f_poblacion f join dim_pais d using (pais_iso3)
           where f.indicador = ?
           group by d.pais order by v2023 desc"""
    , ["pib_per_capita_usd"]).fetchall()

    tabla = "\n".join(
        f"<tr><td>{html.escape(p)}</td><td>{a:,.0f}</td><td>{b:,.0f}</td><td>{(b / a - 1) * 100:+.1f} %</td></tr>"
        for p, a, b in renta
    )

    documento = f"""<!doctype html>
<html lang="es">
<meta charset="utf-8" />
<title>PF-01 · El pulso de dos economías</title>
<style>
  body {{ font-family: Georgia, serif; margin: 2rem auto; max-width: 46rem; color: #1a1a1a; line-height: 1.5; }}
  h1 {{ font-size: 1.9rem; margin-bottom: .2rem; }}
  .nota {{ color: #555; font-size: .85rem; }}
  .grafico {{ width: 100%; height: auto; margin: 1.5rem 0; }}
  .titulo-grafico {{ font-size: 13px; font-weight: bold; }}
  .etiqueta {{ font-size: 12px; }}
  .valor {{ font-size: 10px; fill: #444; }}
  table {{ border-collapse: collapse; width: 100%; margin-top: 1rem; font-size: .9rem; }}
  th, td {{ border-bottom: 1px solid #ddd; padding: .35rem .5rem; text-align: right; }}
  th:first-child, td:first-child {{ text-align: left; }}
  footer {{ margin-top: 2rem; font-size: .8rem; color: #666; }}
</style>
<h1>El pulso de cinco economías</h1>
<p class="nota">Población y PIB per cápita, 2000 frente a 2023. Fuente: Banco Mundial (CC BY 4.0),
descargado el 2026-11-02 con <code>ingerir.py</code>.</p>
{barras(filas, "Población", "personas")}
{barras(renta, "PIB per cápita", "USD corrientes")}
<h2>Renta por persona</h2>
<table>
  <thead><tr><th>País</th><th>2000</th><th>2023</th><th>Cambio</th></tr></thead>
  <tbody>
{tabla}
  </tbody>
</table>
<footer>Dos indicadores no son una economía: falta inflación, paro y PPA. El panel dice lo que
dicen los datos, ni más ni menos.</footer>
</html>
"""
    SALIDA.write_text(documento, encoding="utf-8")
    print(f"  panel escrito: {SALIDA} ({len(documento)} caracteres)")


if __name__ == "__main__":
    main()
