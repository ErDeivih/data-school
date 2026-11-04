CREATE TABLE clientes (id INTEGER, nombre TEXT, ciudad TEXT);
CREATE TABLE pedidos (id INTEGER, cliente_id INTEGER, importe DOUBLE);
INSERT INTO clientes VALUES (1, 'Ana', 'Madrid'), (2, 'Luis', 'Bilbao'), (3, 'Marta', NULL);
INSERT INTO pedidos VALUES (10, 1, 120.50), (11, 1, 30.00), (12, 2, 80.00), (13, 9, 55.00);

-- FULL: los dos descuadres a la vez, la consulta de auditoria por excelencia.
SELECT c.id AS cliente, c.nombre, p.id AS pedido, p.importe
FROM clientes c
FULL OUTER JOIN pedidos p ON p.cliente_id = c.id
ORDER BY c.id NULLS LAST, p.id NULLS LAST;
