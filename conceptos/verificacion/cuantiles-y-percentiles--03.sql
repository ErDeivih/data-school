CREATE TABLE latencias (ms INTEGER);
INSERT INTO latencias VALUES (10),(20),(30),(40),(50),(60),(70),(80),(90),(100);

-- quantile_cont interpola entre valores; quantile_disc solo devuelve valores observados
SELECT count(*)               AS n,
       round(avg(ms), 1)      AS media,
       quantile_cont(ms, 0.5) AS p50,
       quantile_cont(ms, 0.95) AS p95,
       quantile_disc(ms, 0.95) AS p95_orden
FROM latencias;
