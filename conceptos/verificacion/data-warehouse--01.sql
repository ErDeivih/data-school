-- Dos origenes con vocabularios distintos: el almacen los integra en una sola verdad
CREATE TABLE crm AS
SELECT * FROM (VALUES
    ('4471', 'ES', 'Barcelona'),
    ('8890', 'ES', 'Sevilla')
) AS t(id_cliente, codigo_pais, ciudad);

CREATE TABLE facturacion AS
SELECT * FROM (VALUES
    ('4471', 'España', 12050),   -- importe en centimos de euro
    ('8890', 'España',  8000)
) AS t(customer_id, pais, importe_centimos);

CREATE TABLE dim_pais AS
SELECT * FROM (VALUES ('ES', 'España'), ('FR', 'Francia')) AS t(codigo_pais, pais);

-- Hecho integrado: una fila por factura, pais con codigo ISO e importe en euros
CREATE TABLE hechos_ventas AS
SELECT f.customer_id AS nk_cliente, p.codigo_pais, f.importe_centimos / 100.0 AS importe_eur
FROM facturacion f
JOIN dim_pais p ON p.pais = f.pais;

-- Un unico grupo (ES) con las dos ventas: 2 y 200.5
SELECT codigo_pais, count(*) AS ventas, sum(importe_eur) AS total_eur
FROM hechos_ventas
GROUP BY codigo_pais
ORDER BY codigo_pais;
