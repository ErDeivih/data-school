CREATE TABLE pedidos (id INTEGER, cliente TEXT, importe DOUBLE, fecha DATE, ciudad TEXT);
INSERT INTO pedidos VALUES
  (1, 'Ana',   120.50, DATE '2024-01-05', 'Madrid'),
  (2, 'Luis',   80.00, DATE '2024-01-06', NULL),
  (3, 'Ana',   200.00, DATE '2024-01-06', 'Madrid'),
  (4, 'Marta',   NULL, DATE '2024-01-07', 'Sevilla'),
  (5, 'Luis',    45.25, DATE '2024-01-08', NULL);

-- Varias condiciones: el parentesis cambia el resultado, no es decorativo.
SELECT id, ciudad, importe
FROM pedidos
WHERE (ciudad = 'Madrid' OR ciudad = 'Sevilla')
  AND fecha >= DATE '2024-01-06'
ORDER BY fecha, id;

-- Los nulos se ordenan siempre al final, y ademas lo decimos explicitamente.
SELECT id, importe
FROM pedidos
ORDER BY importe ASC NULLS LAST
LIMIT 3;
