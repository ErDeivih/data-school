-- La misma regla, en ELT: el crudo se carga entero y se transforma al consultar.
CREATE TABLE crudo AS
SELECT * FROM (VALUES
    (1, 10,  25.0, 'pagado'),
    (2, 11,  -3.0, 'pagado'),
    (3, 10,  40.0, 'devuelto'),
    (4, 12,  15.0, 'pagado'),
    (5, 13,  NULL, 'pagado'),
    (6, 12,  60.0, 'pagado')
) AS t(pedido_id, cliente_id, importe, estado);

SELECT cliente_id, SUM(importe) AS total
FROM crudo
WHERE estado = 'pagado' AND importe > 0
GROUP BY cliente_id
ORDER BY cliente_id;
