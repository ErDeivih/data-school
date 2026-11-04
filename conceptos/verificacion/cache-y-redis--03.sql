-- Que se cachea y que no se puede cachear: agregados frente a filas que cambian.
CREATE TABLE pedidos (id INTEGER, cliente INTEGER, importe DOUBLE, estado VARCHAR);
-- los tipos son una declaracion: SQLite guarda el valor que le llegue en cada columna

INSERT INTO pedidos VALUES
  (1, 7, 120.50, 'pagado'),
  (2, 7,  80.00, 'pagado'),
  (3, 9,  45.25, 'pendiente'),
  (4, 9, 200.00, 'pagado');

-- Clave de cache: el total pagado por cliente. Cambia poco y se repite mucho.
SELECT cliente, SUM(importe) AS total_pagado
FROM pedidos
WHERE estado = 'pagado'         -- el filtro va antes de agrupar: solo suman los pagados
GROUP BY cliente                -- una fila de salida por cliente
ORDER BY cliente;               -- sin un orden fijo, dos peticiones pueden devolver distinto orden
