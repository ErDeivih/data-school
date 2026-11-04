-- stg_poblacion: una fila por indicador, país y año. Tipos explícitos y sin nulos.
select
    cast(indicador as varchar)          as indicador,
    cast(pais as varchar)               as pais_iso3,
    cast(anio as integer)               as anio,
    cast(valor as double)               as valor,
    cast(descarga as date)              as descargado_en
from read_csv_auto('data/poblacion.csv', header = true)
where valor is not null
  and cast(valor as double) > 0
