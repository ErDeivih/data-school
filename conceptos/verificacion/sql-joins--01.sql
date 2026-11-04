CREATE TABLE clientes (id INTEGER, nombre TEXT, ciudad TEXT);
CREATE TABLE pedidos (id INTEGER, cliente_id INTEGER, importe DOUBLE);
INSERT INTO clientes VALUES (1, 'Ana', 'Madrid'), (2, 'Luis', 'Bilbao'), (3, 'Marta', NULL);
INSERT INTO pedidos VALUES (10, 1, 120.50), (11, 1, 30.00), (12, 2, 80.00);

-- INNER: solo los que tienen pareja. Marta no ha comprado: desaparece.
SELECT p.id, c.nombre, p.importe
FROM pedidos p
JOIN clientes c ON c.id = p.cliente_id
ORDER BY p.id;
