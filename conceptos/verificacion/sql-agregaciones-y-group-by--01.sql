-- Una agregacion minima: una fila por ciudad y solo los grupos que facturan mas de 100.
CREATE TABLE ventas (id INTEGER, ciudad VARCHAR, importe DECIMAL(10,2));

INSERT INTO ventas VALUES
    (1, 'Madrid',   75.00),
    (2, 'Madrid',  150.00),
    (3, 'Sevilla',  25.00),
    (4, 'Sevilla', 400.00),
    (5, 'Bilbao',   30.00),
    (6, 'Bilbao',   NULL);

SELECT ciudad,
       COUNT(*)               AS pedidos,
       COUNT(importe)         AS con_importe,
       SUM(importe)           AS facturado,
       ROUND(AVG(importe), 2) AS ticket_medio
FROM ventas
GROUP BY ciudad
HAVING SUM(importe) > 100
ORDER BY facturado DESC;
