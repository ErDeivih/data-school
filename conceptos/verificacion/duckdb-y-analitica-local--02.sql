-- Analitica local: SQL con funciones de ventana sobre datos que crea el propio bloque.
CREATE TABLE pedidos AS
SELECT * FROM (VALUES
    ('2024-01-05', 'ana',  120.0),
    ('2024-01-19', 'ana',   80.0),
    ('2024-02-15', 'ana',   40.0),
    ('2024-02-02', 'luis', 200.0),
    ('2024-03-01', 'luis', 100.0)
) AS t(fecha, cliente, importe);

SELECT cliente,
       fecha,
       importe,
       SUM(importe) OVER (PARTITION BY cliente ORDER BY fecha) AS acumulado
FROM pedidos
ORDER BY cliente, fecha;
