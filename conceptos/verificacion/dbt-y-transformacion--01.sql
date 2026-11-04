-- El mismo incremental, en SQL puro, para ver por que es idempotente.
CREATE TABLE raw_pedidos AS
SELECT * FROM (VALUES
    (DATE '2024-03-01', 'P1', 100.0, 'ok'),
    (DATE '2024-03-01', 'P2', 250.0, 'cancelado'),
    (DATE '2024-03-02', 'P3', 80.0,  'ok'),
    (DATE '2024-03-02', 'P4', 120.0, 'ok')
) AS t(fecha, pedido_id, importe, estado);

-- Primera ejecucion: la tabla entera (equivale a un --full-refresh)
CREATE TABLE fact_ventas_diarias AS
SELECT fecha, sum(importe) AS total, count(*) AS pedidos
FROM raw_pedidos WHERE estado = 'ok' GROUP BY fecha;

-- Siguiente ejecucion: solo la particion nueva, reconstruida y reemplazada
CREATE OR REPLACE TABLE nuevo AS
SELECT fecha, sum(importe) AS total, count(*) AS pedidos
FROM raw_pedidos WHERE estado = 'ok' AND fecha = DATE '2024-03-02' GROUP BY fecha;

DELETE FROM fact_ventas_diarias WHERE fecha IN (SELECT fecha FROM nuevo);
INSERT INTO fact_ventas_diarias SELECT * FROM nuevo;

SELECT * FROM fact_ventas_diarias ORDER BY fecha;
