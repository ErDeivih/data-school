CREATE TABLE clientes (id INTEGER, nombre TEXT, ciudad TEXT);
CREATE TABLE pedidos (id INTEGER, cliente_id INTEGER, importe DOUBLE);
INSERT INTO clientes VALUES (1, 'Ana', 'Madrid'), (2, 'Luis', 'Bilbao'), (3, 'Marta', NULL);
INSERT INTO pedidos VALUES (10, 1, 120.50), (11, 1, 30.00), (12, 2, 80.00);

-- count(*) cuenta filas del resultado (Marta aporta una sin pedido);
-- count(p.id) cuenta pedidos de verdad, porque ignora los NULL.
SELECT
  c.ciudad,
  count(*)      AS filas_del_join,
  count(p.id)   AS pedidos_reales,
  round(sum(p.importe), 2) AS total
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
GROUP BY c.ciudad
ORDER BY c.ciudad NULLS LAST;
