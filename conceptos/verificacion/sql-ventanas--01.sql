-- La misma ventana con RANGE (defecto) y con ROWS: solo cambia el marco.
CREATE TABLE ventas (fecha DATE, importe INTEGER);

INSERT INTO ventas VALUES
    ('2024-01-01', 10),
    ('2024-01-02', 20),
    ('2024-01-02', 30),
    ('2024-01-03', 40);

SELECT fecha,
       importe,
       SUM(importe) OVER (ORDER BY fecha) AS acumulado_rango,
       SUM(importe) OVER (ORDER BY fecha
                          ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS acumulado_filas,
       ROUND(AVG(importe) OVER (ORDER BY fecha
                                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS media_movil_3,
       LAG(importe) OVER (ORDER BY fecha) AS importe_anterior
FROM ventas
ORDER BY fecha, importe;
