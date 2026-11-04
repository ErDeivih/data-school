CREATE TABLE pedidos (usuario VARCHAR, fecha DATE);
INSERT INTO pedidos VALUES
  ('ana', '2026-01-03'), ('ana', '2026-01-19'), ('ana', '2026-02-02'),
  ('luis', '2026-01-07'), ('luis', '2026-01-28'), ('marta', '2026-02-11');

-- Numero las filas dentro de cada usuario: la 2 es su segundo pedido.
SELECT usuario, fecha AS segundo_pedido
FROM (SELECT usuario, fecha, ROW_NUMBER() OVER (PARTITION BY usuario ORDER BY fecha) AS n FROM pedidos)
WHERE n = 2
ORDER BY usuario;
