-- Cesta de la compra: tickets resumidos y asociaciones entre pares de articulos.
CREATE TABLE tickets AS
SELECT * FROM (VALUES
    (1, 'pan'), (1, 'mantequilla'), (1, 'leche'),
    (2, 'pan'), (2, 'mantequilla'),
    (3, 'pan'), (3, 'leche'),
    (4, 'pan'), (4, 'mantequilla'),
    (5, 'leche'), (5, 'cafe')
) AS t(ticket, articulo);

WITH total AS (SELECT count(DISTINCT ticket) AS n FROM tickets),
     item AS (SELECT articulo, count(DISTINCT ticket) AS n_item FROM tickets GROUP BY articulo),
     par AS (
        SELECT a.articulo AS x, b.articulo AS y, count(DISTINCT a.ticket) AS n_par
        FROM tickets a
        JOIN tickets b ON a.ticket = b.ticket AND a.articulo < b.articulo  -- el < quita el par repetido
        GROUP BY a.articulo, b.articulo
     )
SELECT par.x, par.y,
       round(par.n_par / total.n, 3) AS soporte,
       round(par.n_par * 1.0 / item_x.n_item, 3) AS confianza,
       round((par.n_par * 1.0 / item_x.n_item) / (item_y.n_item * 1.0 / total.n), 3) AS lift
FROM par
JOIN total ON true
JOIN item AS item_x ON item_x.articulo = par.x
JOIN item AS item_y ON item_y.articulo = par.y
ORDER BY lift DESC;
