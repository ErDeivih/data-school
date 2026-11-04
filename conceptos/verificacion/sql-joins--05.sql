CREATE TABLE clientes (id INTEGER, nombre TEXT, ciudad TEXT);
CREATE TABLE pedidos (id INTEGER, cliente_id INTEGER, importe DOUBLE);
INSERT INTO clientes VALUES (1, 'Ana', 'Madrid'), (2, 'Luis', 'Bilbao'), (3, 'Marta', NULL);
INSERT INTO pedidos VALUES (10, 1, 120.50), (11, 1, 30.00), (12, 2, 80.00), (13, 9, 55.00);

-- Autocombinacion: los pedidos de un mismo cliente, por parejas.
SELECT a.id AS pedido_a, b.id AS pedido_b, a.importe + b.importe AS suma
FROM pedidos a
JOIN pedidos b ON a.cliente_id = b.cliente_id AND a.id < b.id
ORDER BY a.id;

-- Anti-union: lo que falta en el otro lado, sin usar NOT IN (que falla con nulos).
SELECT c.id, c.nombre
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
WHERE p.id IS NULL;
