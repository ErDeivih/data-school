-- Catalogo de particiones de una tabla: 24 meses de 8 GB cada uno.
CREATE TABLE particiones AS
SELECT m AS mes, 8.0 AS gb FROM generate_series(1, 24) AS t(m);

-- Una consulta que filtra tres meses: el motor solo abre esas particiones.
SELECT count(*) AS particiones,
       round(sum(gb), 1) AS gb_totales,
       round(sum(CASE WHEN mes <= 3 THEN gb ELSE 0 END), 1) AS gb_leidos
FROM particiones;
