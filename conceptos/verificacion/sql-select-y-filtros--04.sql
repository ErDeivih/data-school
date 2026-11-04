CREATE TABLE pedidos (id INTEGER, importe DOUBLE);
INSERT INTO pedidos VALUES (1, 10.0), (2, NULL), (3, 30.0);

-- Donde cae el nulo al ordenar: en DuckDB, NULLS LAST es el comportamiento
-- por defecto en ASC y en DESC. Escribirlo evita depender del motor.
SELECT id, importe FROM pedidos ORDER BY importe DESC NULLS LAST;
