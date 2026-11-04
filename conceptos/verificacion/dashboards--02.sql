-- Un panel no necesita una consulta por grafico: esta devuelve la metrica, su valor
-- anterior y la variacion, y solo de los ultimos dias.
CREATE TABLE pedidos (fecha DATE, pedidos INTEGER, cancelados INTEGER);

INSERT INTO pedidos VALUES
    ('2024-05-01', 420, 12), ('2024-05-02', 455, 9), ('2024-05-03', 480, 14),
    ('2024-05-04', 300, 6),  ('2024-05-05', 285, 5), ('2024-05-06', 501, 22),
    ('2024-05-07', 470, 11);

SELECT fecha,
       pedidos,
       ROUND(100.0 * cancelados / pedidos, 2) AS cancelacion_pct,
       pedidos - LAG(pedidos) OVER (ORDER BY fecha) AS delta_ayer
FROM pedidos
ORDER BY fecha DESC
LIMIT 3;
