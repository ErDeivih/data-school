-- Cada hecho en un solo sitio: el nombre del cliente no se repite en pedidos,
-- y el precio de venta se guarda en la linea, donde es un hecho historico.
CREATE TABLE clientes (cliente_id INTEGER PRIMARY KEY, nombre VARCHAR, ciudad VARCHAR);
CREATE TABLE pedidos  (pedido_id INTEGER PRIMARY KEY, cliente_id INTEGER, fecha DATE);
CREATE TABLE lineas   (pedido_id INTEGER, producto_id INTEGER,
                       unidades INTEGER, precio_unitario DECIMAL(10,2));

INSERT INTO clientes VALUES (1, 'Ana', 'Valencia'), (2, 'Luis', 'Bilbao');
INSERT INTO pedidos VALUES
    (1001, 1, DATE '2024-02-01'), (1002, 1, DATE '2024-02-03'),
    (1003, 2, DATE '2024-02-05'), (1004, 2, DATE '2024-02-07');
INSERT INTO lineas VALUES
    (1001, 10, 2,  25.00), (1002, 11, 1,  15.00),
    (1003, 10, 1,  25.00), (1004, 12, 2, 180.00);

SELECT c.nombre,
       c.ciudad,
       COUNT(*) AS lineas,
       SUM(l.unidades * l.precio_unitario) AS total
FROM pedidos p
JOIN clientes c ON c.cliente_id = p.cliente_id
JOIN lineas   l ON l.pedido_id = p.pedido_id
GROUP BY c.nombre, c.ciudad
ORDER BY total DESC;
