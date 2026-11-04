-- El modelo copiado permite que un cliente tenga dos ciudades a la vez
CREATE TABLE pedidos AS
SELECT * FROM (VALUES
    (1, 4471, 'Madrid',    120.00),
    (2, 4471, 'Barcelona',  80.00),
    (3, 8890, 'Sevilla',    50.00)
) AS t(id_pedido, nk_cliente, ciudad, importe);

-- El cliente 4471 aparece dos veces: 80.0 y 120.0 repartidos entre dos ciudades
SELECT nk_cliente, ciudad, sum(importe) AS total
FROM pedidos
GROUP BY nk_cliente, ciudad
ORDER BY nk_cliente, ciudad;
