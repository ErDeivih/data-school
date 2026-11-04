CREATE TABLE pedidos (id INTEGER, cliente TEXT, importe DOUBLE, fecha DATE, ciudad TEXT);
INSERT INTO pedidos VALUES
  (1, 'Ana',   120.50, DATE '2024-01-05', 'Madrid'),
  (2, 'Luis',   80.00, DATE '2024-01-06', NULL),
  (3, 'Ana',   200.00, DATE '2024-01-06', 'Madrid'),
  (4, 'Marta',   NULL, DATE '2024-01-07', 'Sevilla'),
  (5, 'Luis',    45.25, DATE '2024-01-08', NULL);

-- El filtro deja fuera los nulos: desconocido no es verdadero.
SELECT id, cliente, importe
FROM pedidos
WHERE importe > 100
ORDER BY importe DESC;
