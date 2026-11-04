CREATE TABLE pedidos (id INTEGER, fecha DATE, importe DOUBLE);
INSERT INTO pedidos VALUES
  (1, DATE '2024-01-05', 120.50), (2, DATE '2024-01-06', 80.00),
  (3, DATE '2024-01-06', 200.00), (4, DATE '2024-01-07', NULL),
  (5, DATE '2024-01-08', 45.25);

-- Fechas y tipos: se comparan con el tipo correcto, no con una cadena.
SELECT fecha, count(*) AS pedidos, round(sum(importe), 2) AS total
FROM pedidos
WHERE fecha >= DATE '2024-01-06' AND importe IS NOT NULL
GROUP BY fecha
ORDER BY fecha;

-- CAST explicito: si el importe llega como texto, se convierte antes de sumar.
SELECT sum(CAST('150.25' AS DOUBLE)) AS suma_convertida;
