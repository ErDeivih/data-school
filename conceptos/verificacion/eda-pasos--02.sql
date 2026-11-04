-- El grano importa: sumar por la clave equivocada multiplica los totales.
CREATE TABLE lineas(pedido_id INTEGER, linea INTEGER, importe DOUBLE);
INSERT INTO lineas VALUES (1,1,10.0),(1,2,5.5),(2,1,20.0),(3,1,7.25);

SELECT count(*) AS filas,
       round(sum(importe), 2) AS total_lineas,
       count(DISTINCT pedido_id) AS pedidos,
       round(sum(importe) / count(DISTINCT pedido_id), 2) AS ticket_medio
FROM lineas;
