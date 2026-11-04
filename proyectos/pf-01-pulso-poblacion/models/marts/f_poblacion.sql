-- f_poblacion: grano indicador + país + año. Solo los indicadores que sabemos leer.
select
    indicador,
    pais_iso3,
    anio,
    valor
from {{ ref('stg_poblacion') }}
where indicador in ('poblacion', 'pib_per_capita_usd')
