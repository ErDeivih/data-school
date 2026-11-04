# PF-01 · El pulso de dos economías con datos públicos

**Estado:** completo el 2026-11-02. Ingesta, modelo, pruebas y panel, con datos reales.

## La pregunta

¿Cuánto ha cambiado la población y la renta por persona en cinco economías europeas entre 2000 y
2023, y qué parte de esa historia se puede contar sin engañar?

## La fuente

Banco Mundial, API abierta (`api.worldbank.org`). Dos indicadores y cinco países:

| Indicador | Código | Unidad |
| --- | --- | --- |
| Población total | `SP.POP.TOTL` | personas |
| PIB per cápita | `NY.GDP.PCAP.CD` | USD corrientes |

Países: ESP, FRA, DEU, ITA, PRT. Años: 2000-2023. Licencia: CC BY 4.0.

## Cómo se ejecuta

```sh
python ingerir.py     # descarga, guarda el bruto y escribe data/poblacion.csv (240 filas)
python modelar.py     # construye stg_poblacion, dim_pais y f_poblacion + 7 pruebas
python panel.py       # escribe panel.html, que se abre con doble clic
python verificar.py   # 11 comprobaciones de la ingesta
```

## Capas

```
data/raw/*.json          bruto inmutable, con fecha de descarga
data/poblacion.csv       tabla larga: indicador, país, año, valor
models/staging/          stg_poblacion.sql   (limpieza y tipos)
models/marts/            dim_pais.sql, f_poblacion.sql
models/schema.yml        pruebas de dbt: not_null, unique, accepted_values, relationships
modelar.py               ejecuta los modelos con DuckDB y sus pruebas (7 en verde)
panel.html               dos gráficos SVG y una tabla, sin servidor ni dependencias
```

Es un **proyecto dbt de verdad** (`dbt_project.yml`, `models/`, `schema.yml`). Como aquí solo está
el adaptador de Postgres, `modelar.py` ejecuta el mismo SQL con DuckDB; con `dbt-duckdb` instalado,
`dbt build` haría exactamente eso.

## Lo que dicen los datos

| País | Población 2000 | Población 2023 | PIB por persona 2000 | PIB por persona 2023 |
| --- | --- | --- | --- | --- |
| España | 40,57 M | 48,35 M | 14.743 USD | 33.493 USD (+127 %) |
| Alemania | 82,21 M | 83,29 M | 23.926 USD | 54.777 USD (+129 %) |
| Francia | 60,92 M | 68,37 M | 22.341 USD | 44.700 USD (+100 %) |
| Italia | 56,94 M | 58,98 M | 20.190 USD | 39.280 USD (+95 %) |
| Portugal | 10,29 M | 10,58 M | 11.526 USD | 27.635 USD (+140 %) |

La historia interesante no es el crecimiento, es la composición: España crece un 19 % en población
y Alemania un 1,3 %, pero las dos multiplican su renta por 2,3. Un país crece por gente o por
productividad, y la tabla los separa.

## Decisiones y por qué

- **Tabla larga.** Añadir un indicador no cambia el esquema.
- **Bruto con fecha.** El CSV se reconstruye; el bruto no se toca.
- **Dimensiones y hecho.** `dim_pais` da el nombre; el hecho guarda la clave. Es el modelo en
  estrella mínimo que se pide en cualquier entrevista.
- **Pruebas en el modelo, no solo en el script.** Unicidad de la dimensión, integridad referencial
  y unicidad del hecho por indicador, país y año.
- **Panel sin servidor.** Un HTML con SVG se abre con doble clic y no depende de nada.

## Límites, dichos a propósito

- Dos indicadores no son una economía: faltan inflación, paro y PPA.
- Dólares corrientes mezclan renta con tipo de cambio.
- 2023 puede ser provisional en algunos países; el bruto permite comprobarlo.
- No hay orquestación todavía: cuatro comandos a mano.

## Qué se aprende

`ingesta-incremental-y-cdc`, `modelado-dimensional`, `dbt-y-transformacion`,
`contratos-de-datos`, `visualizacion-honesta` y `reconciliacion-y-pruebas`.
