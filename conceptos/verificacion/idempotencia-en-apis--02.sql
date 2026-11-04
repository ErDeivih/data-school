-- La clave del cliente es la clave primaria: la base de datos, no el codigo, impide el duplicado.
CREATE TABLE pagos (clave VARCHAR PRIMARY KEY, importe DECIMAL(10,2));

INSERT INTO pagos VALUES ('pay-001', 250.00);
INSERT INTO pagos VALUES ('pay-002', 90.00);
-- El ON CONFLICT convierte el reintento en una operacion segura: no duplica ni falla.
INSERT INTO pagos VALUES ('pay-001', 250.00) ON CONFLICT DO NOTHING;

SELECT count(*) AS pagos, sum(importe) AS total FROM pagos;
