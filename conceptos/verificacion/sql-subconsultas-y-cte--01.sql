-- Encadenar dos CTE es lo que permite leer la consulta en el orden en que se piensa.
CREATE TABLE pedidos (id INTEGER, cliente VARCHAR, importe INTEGER);

INSERT INTO pedidos VALUES
    (1, 'Ana',   100), (2, 'Ana',    50),
    (3, 'Luis',  200), (4, 'Luis',  300),
    (5, 'Marta', 400), (6, NULL,     80);

WITH por_cliente AS (
    SELECT cliente, SUM(importe) AS total, COUNT(*) AS pedidos
    FROM pedidos
    WHERE cliente IS NOT NULL
    GROUP BY cliente
),
referencia AS (
    SELECT AVG(importe) AS pedido_medio FROM pedidos
)
SELECT p.cliente, p.total, p.pedidos, ROUND(r.pedido_medio, 2) AS pedido_medio
FROM por_cliente p
CROSS JOIN referencia r
WHERE p.total > r.pedido_medio
ORDER BY p.total DESC;
