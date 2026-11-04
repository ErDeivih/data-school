-- Reproceso idempotente de UNA particion: se reconstruye entera y se reemplaza.
CREATE TABLE ventas AS
SELECT * FROM (VALUES
    (DATE '2024-01-01', 'P1', 100.0, 0.21),
    (DATE '2024-01-01', 'P2', 250.0, 0.10)
) AS t(fecha, pedido_id, base, iva);

-- Logica corregida: el IVA se calcula sobre la base de cada linea y se redondea a centimos
-- antes de agregar, que es como se factura.
CREATE OR REPLACE TABLE fact_ventas AS
SELECT fecha, sum(base) + sum(round(base * iva, 2)) AS total
FROM ventas WHERE fecha = DATE '2024-01-01' GROUP BY fecha;

-- El reproceso se relanza (o se lanza tres veces): el resultado no cambia.
CREATE OR REPLACE TABLE fact_ventas AS
SELECT fecha, sum(base) + sum(round(base * iva, 2)) AS total
FROM ventas WHERE fecha = DATE '2024-01-01' GROUP BY fecha;

SELECT * FROM fact_ventas;
