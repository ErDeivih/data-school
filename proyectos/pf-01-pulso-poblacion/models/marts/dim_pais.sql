-- dim_pais: una fila por país, con su nombre. El ISO3 es la clave.
select
    pais_iso3,
    case pais_iso3
        when 'ESP' then 'España'
        when 'FRA' then 'Francia'
        when 'DEU' then 'Alemania'
        when 'ITA' then 'Italia'
        when 'PRT' then 'Portugal'
        else pais_iso3
    end as pais
from (select distinct pais_iso3 from {{ ref('stg_poblacion') }})
