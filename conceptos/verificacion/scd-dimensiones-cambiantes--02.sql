-- Con la clave sustitutiva en los hechos, cada venta cae en su version historica
CREATE TABLE dim_cliente AS
SELECT * FROM (VALUES
    (9001, 4471, 'Madrid',    DATE '2019-01-01', DATE '2022-03-15', FALSE),
    (9002, 4471, 'Barcelona', DATE '2022-03-15', DATE '2024-07-01', FALSE),
    (9003, 4471, 'Valencia',  DATE '2024-07-01', DATE '9999-12-31', TRUE)
) AS t(sk, nk, ciudad, inicio, fin, actual);

CREATE TABLE hechos_ventas AS
SELECT * FROM (VALUES
    (DATE '2023-05-02', 9002, 120.50),
    (DATE '2025-02-10', 9003,  80.00)
) AS t(fecha, sk_cliente, importe);

-- Informe historico: Barcelona 120.50 y Valencia 80.00, dos filas y ningun doble conteo
SELECT d.ciudad, count(*) AS ventas, sum(f.importe) AS total
FROM hechos_ventas f
JOIN dim_cliente d ON d.sk = f.sk_cliente
GROUP BY d.ciudad
ORDER BY d.ciudad;
