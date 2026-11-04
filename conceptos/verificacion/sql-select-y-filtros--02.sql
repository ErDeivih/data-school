CREATE TABLE pedidos (id INTEGER, importe DOUBLE, ciudad TEXT);
INSERT INTO pedidos VALUES
  (1, 120.50, 'Madrid'), (2, 80.00, NULL), (3, 200.00, 'Madrid'),
  (4, NULL, 'Sevilla'), (5, 45.25, NULL);

-- count(*) cuenta filas; count(columna) ignora los nulos. No son lo mismo.
SELECT
  count(*)                     AS filas,
  count(importe)               AS importes_no_nulos,
  count(*) - count(importe)    AS nulos,
  round(sum(importe), 2)       AS suma,
  round(avg(importe), 2)       AS media_sin_nulos,
  round(avg(coalesce(importe, 0)), 2) AS media_contando_cero
FROM pedidos;
