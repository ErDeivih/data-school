CREATE TABLE eventos (id INTEGER, usuario VARCHAR, tipo VARCHAR, fecha DATE);

INSERT INTO eventos VALUES
  (1, 'u1', 'visita', DATE '2024-01-10'),
  (2, 'u1', 'compra', DATE '2024-02-02'),
  (3, 'u2', 'compra', DATE '2026-01-05');

-- Politica de retencion: los eventos de analitica se borran a los 24 meses.
DELETE FROM eventos WHERE fecha < DATE '2026-01-01';

SELECT usuario, count(*) AS eventos_conservados FROM eventos GROUP BY usuario ORDER BY usuario;
