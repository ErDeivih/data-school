CREATE TABLE destino (pedido_id VARCHAR PRIMARY KEY, importe INTEGER);

-- Primer intento
INSERT INTO destino VALUES ('P1', 100), ('P2', 250);
-- El orquestador no recibe respuesta y reintenta: mismas filas, misma clave
INSERT INTO destino VALUES ('P1', 100), ('P2', 250) ON CONFLICT (pedido_id) DO NOTHING;
-- Y un tercer intento
INSERT INTO destino VALUES ('P1', 100), ('P2', 250) ON CONFLICT (pedido_id) DO NOTHING;

SELECT count(*) AS filas, sum(importe) AS suma FROM destino;
