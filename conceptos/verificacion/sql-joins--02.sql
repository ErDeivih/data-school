CREATE TABLE clientes (id INTEGER, nombre TEXT, ciudad TEXT);
CREATE TABLE pedidos (id INTEGER, cliente_id INTEGER, importe DOUBLE);
INSERT INTO clientes VALUES (1, 'Ana', 'Madrid'), (2, 'Luis', 'Bilbao'), (3, 'Marta', NULL);
INSERT INTO pedidos VALUES (10, 1, 120.50), (11, 1, 30.00), (12, 2, 80.00);

-- LEFT: todos los clientes, tengan pedidos o no. Marta sale con NULL.
SELECT c.id, c.nombre, p.id AS pedido, p.importe
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
ORDER BY c.id, p.id;
