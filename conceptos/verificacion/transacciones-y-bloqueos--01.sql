CREATE TABLE cuentas (id VARCHAR, saldo DECIMAL(10,2));
INSERT INTO cuentas VALUES ('A', 500.00), ('B', 300.00);
CREATE TABLE registro (paso VARCHAR, saldo_a DECIMAL(10,2), saldo_b DECIMAL(10,2));

-- 1) Media transferencia que se aborta: el cargo queda deshecho.
BEGIN TRANSACTION;
UPDATE cuentas SET saldo = saldo - 200.00 WHERE id = 'A';
ROLLBACK;
INSERT INTO registro SELECT 'tras el rollback',
    (SELECT saldo FROM cuentas WHERE id = 'A'), (SELECT saldo FROM cuentas WHERE id = 'B');

-- 2) La transferencia entera: las dos escrituras se confirman juntas.
BEGIN TRANSACTION;
UPDATE cuentas SET saldo = saldo - 200.00 WHERE id = 'A';
UPDATE cuentas SET saldo = saldo + 200.00 WHERE id = 'B';
COMMIT;
INSERT INTO registro SELECT 'tras el commit',
    (SELECT saldo FROM cuentas WHERE id = 'A'), (SELECT saldo FROM cuentas WHERE id = 'B');

-- 3) Sin transaccion, el abono no encuentra destino y no avisa: 0 filas afectadas.
UPDATE cuentas SET saldo = saldo - 200.00 WHERE id = 'A';
UPDATE cuentas SET saldo = saldo + 200.00 WHERE id = 'ZZ';
INSERT INTO registro SELECT 'sin transaccion',
    (SELECT saldo FROM cuentas WHERE id = 'A'), (SELECT saldo FROM cuentas WHERE id = 'B');

SELECT * FROM registro;
