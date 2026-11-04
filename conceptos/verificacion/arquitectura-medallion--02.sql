-- Bronce guarda lo que llego; plata limpia y deduplica; oro agrega para el negocio.
WITH bronce(pedido_id, fecha, cliente, importe, pais) AS (
    VALUES
        (1, DATE '2024-01-02', 'ana',   10.5,  'ES'),
        (2, DATE '2024-01-02', 'luis',  20.0,  'ES'),
        (2, DATE '2024-01-02', 'luis',  20.0,  'ES'),   -- duplicado de la ingesta
        (3, DATE '2024-01-03', 'ana',   NULL,  'ES'),   -- importe que no llego
        (4, DATE '2024-01-03', 'marta', 5.25,  'FR')
),
plata AS (
    SELECT DISTINCT pedido_id, fecha, cliente, importe, pais
    FROM bronce
    WHERE importe IS NOT NULL
)
SELECT pais, count(*) AS pedidos, round(sum(importe), 2) AS facturado
FROM plata
GROUP BY pais
ORDER BY pais;
