import test from "node:test";
import assert from "node:assert/strict";
import { extractLinks, normalizeUrl, classify, buildReport } from "./check-links.mjs";

test("extrae enlaces Markdown con su línea y su texto", () => {
  const md = ["# Título", "", "Una [fuente buena](https://example.com/a) y otra.", "[docs](https://example.com/b)"].join("\n");
  const links = extractLinks(md);
  assert.equal(links.length, 2);
  assert.deepEqual(links[0], { url: "https://example.com/a", line: 3, text: "fuente buena" });
  assert.equal(links[1].line, 4);
});

test("deduplica enlaces repetidos y limpia puntuación final", () => {
  const md = "[a](https://example.com/x). [b](https://example.com/x) https://example.com/x";
  const links = extractLinks(md);
  assert.equal(links.length, 1);
  assert.equal(links[0].url, "https://example.com/x");
});

test("recoge URLs sueltas sin duplicar las que ya eran enlace", () => {
  const md = "[a](https://example.com/a) y luego https://example.com/b en texto.";
  const links = extractLinks(md);
  assert.deepEqual(links.map((l) => l.url), ["https://example.com/a", "https://example.com/b"]);
});

test("ignora mailto, anclas y javascript", () => {
  const md = "[correo](mailto:a@b.c) [ancla](#seccion) [js](javascript:void(0))";
  assert.equal(extractLinks(md).length, 0);
});

test("normaliza la URL para comparar redirecciones", () => {
  assert.equal(normalizeUrl("HTTPS://Example.com/ruta/"), normalizeUrl("https://example.com/ruta"));
  assert.notEqual(normalizeUrl("https://example.com/ruta"), normalizeUrl("https://example.com/otra"));
});

test("añadir parámetros de seguimiento no cuenta como redirección", () => {
  const tracked = classify(200, {
    originalUrl: "https://www.youtube.com/@statquest",
    finalUrl: "https://www.youtube.com/@statquest?cbrd=1&ucbcb=1",
  });
  assert.equal(tracked.state, "vivo");
});

test("clasifica vivo, redirige, bloqueado, caído y error", () => {
  assert.equal(classify(200, { originalUrl: "https://a.es", finalUrl: "https://a.es" }).state, "vivo");
  assert.equal(classify(200, { originalUrl: "https://a.es", finalUrl: "https://a.es/" }).state, "vivo");
  const moved = classify(200, { originalUrl: "https://a.es", finalUrl: "https://b.es/nuevo" });
  assert.equal(moved.state, "redirige");
  assert.match(moved.note, /b\.es\/nuevo/);
  assert.equal(classify(403, { originalUrl: "https://a.es" }).state, "bloqueado");
  assert.equal(classify(429, { originalUrl: "https://a.es" }).state, "bloqueado");
  assert.equal(classify(404, { originalUrl: "https://a.es" }).state, "caído");
  assert.equal(classify(410, { originalUrl: "https://a.es" }).state, "caído");
  assert.equal(classify(503, { originalUrl: "https://a.es" }).state, "error");
  assert.equal(classify(0, { error: "ECONNREFUSED" }).state, "error");
  assert.equal(classify(0, { error: "ECONNREFUSED" }).code, 0);
});

test("el informe ordena por gravedad y cuenta estados", () => {
  const results = [
    { url: "https://a.es", state: "vivo", code: 200 },
    { url: "https://b.es", state: "caído", code: 404, note: "el recurso ya no existe" },
    { url: "https://c.es", state: "bloqueado", code: 403, note: "rechaza bots" },
  ];
  const report = buildReport(results, { files: ["FUENTES.md"], date: new Date("2026-11-04T10:00:00Z") });
  assert.match(report, /Informe de enlaces — 2026-11-04/);
  assert.match(report, /\*\*caídos\*\*: 1/);
  assert.match(report, /\*\*bloqueados \(revisar a mano\)\*\*: 1/);
  const indexDead = report.indexOf("https://b.es");
  const indexOk = report.indexOf("https://a.es");
  assert.ok(indexDead >= 0 && indexOk >= 0 && indexDead < indexOk, "el caído va antes que el vivo");
});
