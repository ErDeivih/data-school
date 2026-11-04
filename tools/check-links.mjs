#!/usr/bin/env node
/**
 * Comprobador de enlaces de Data School.
 *
 * Extrae los enlaces de un Markdown, los comprueba de verdad (HTTP), los clasifica
 * y escribe un informe fechado en INFORMES/. Sin dependencias: solo Node 20+.
 *
 * Uso:
 *   node tools/check-links.mjs                       # comprueba FUENTES.md
 *   node tools/check-links.mjs --file FUENTES.md --file INVESTIGACION.md
 *   node tools/check-links.mjs --json                # solo el JSON, para pipes
 *   node tools/check-links.mjs --strict              # sale con 1 si hay caídos
 *
 * Clasificación (y por qué no es "200 = bien, 404 = mal"):
 *   vivo        responde 2xx/3xx y sirve el mismo recurso
 *   redirige    responde, pero el recurso se ha movido (posible cambio de dominio)
 *   bloqueado   401/403/429/999: el sitio rechaza la comprobación automatizada.
 *               NO se puede declarar muerto por esto: se marca para revisión manual.
 *   caído       404/410/451: el recurso ya no existe
 *   error       fallo de red o 5xx tras reintento: no concluyente
 */

import { readFile, writeFile, mkdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const USER_AGENT =
  "Mozilla/5.0 (compatible; DataSchoolLinkChecker/1.0; +https://github.com/ErDeivih/data-school)";
const DEFAULT_TIMEOUT_MS = 20000;
const DEFAULT_CONCURRENCY = 6;
const RETRY_DELAY_MS = 700;

const MARKDOWN_LINK = /\[([^\]]*)\]\((https?:\/\/[^)\s]+)\)/g;
const BARE_URL = /https?:\/\/[^\s<>"'`)\]]+/g;
const SKIP_PREFIXES = ["mailto:", "#", "tel:", "javascript:"];

/** Extrae enlaces únicos de un Markdown, con su línea y su texto. */
export function extractLinks(markdown) {
  const found = [];
  const seen = new Set();
  const push = (url, line, text) => {
    const clean = url.replace(/[.,;:]$/, "");
    if (!clean.startsWith("http")) return;
    if (SKIP_PREFIXES.some((p) => clean.startsWith(p))) return;
    if (seen.has(clean)) return;
    seen.add(clean);
    found.push({ url: clean, line, text: (text || "").trim() });
  };
  const lineAt = (index) => markdown.slice(0, index).split("\n").length;

  for (const match of markdown.matchAll(MARKDOWN_LINK)) {
    push(match[2], lineAt(match.index ?? 0), match[1]);
  }
  for (const match of markdown.matchAll(BARE_URL)) {
    push(match[0], lineAt(match.index ?? 0), "");
  }
  return found;
}

/** Clave estable para comparar la URL pedida con la final tras redirecciones.
 *  Ignora la query (los parámetros de seguimiento tipo ?utm/&cbrd no son un traslado
 *  del recurso) y el hash. Solo un cambio de host o de ruta cuenta como redirección. */
export function normalizeUrl(raw) {
  try {
    const url = new URL(raw);
    const path = url.pathname.replace(/\/+$/, "");
    return `${url.host.toLowerCase()}${path}`;
  } catch {
    return String(raw);
  }
}

/** Clasifica el resultado de una petición. */
export function classify(status, info = {}) {
  const { originalUrl = "", finalUrl = "", error = "" } = info;
  if (error) {
    return { state: "error", code: 0, note: `sin respuesta: ${error}` };
  }
  if (!status) {
    return { state: "error", code: 0, note: "sin código de estado" };
  }
  if (status >= 200 && status < 400) {
    if (finalUrl && normalizeUrl(finalUrl) !== normalizeUrl(originalUrl)) {
      return {
        state: "redirige",
        code: status,
        note: `ahora vive en ${finalUrl}`,
      };
    }
    return { state: "vivo", code: status, note: "" };
  }
  if ([401, 403, 429, 999].includes(status)) {
    return {
      state: "bloqueado",
      code: status,
      note: "rechaza la comprobación automatizada; verificar a mano",
    };
  }
  if ([404, 410, 451].includes(status)) {
    return { state: "caído", code: status, note: "el recurso ya no existe" };
  }
  if (status >= 500) {
    return { state: "error", code: status, note: "error del servidor tras reintento" };
  }
  return { state: "error", code: status, note: "respuesta no concluyente" };
}

/** Comprueba una URL con reintento en fallos de red o 5xx. */
export async function checkUrl(url, options = {}) {
  const { timeoutMs = DEFAULT_TIMEOUT_MS, retries = 1 } = options;
  let last = { state: "error", code: 0, note: "sin intentos" };
  for (let attempt = 0; attempt <= retries; attempt += 1) {
    const startedAt = Date.now();
    try {
      const res = await fetch(url, {
        redirect: "follow",
        headers: { "user-agent": USER_AGENT, accept: "text/html,application/xhtml+xml,*/*;q=0.8" },
        signal: AbortSignal.timeout(timeoutMs),
      });
      await res.body?.cancel().catch(() => {});
      last = { ...classify(res.status, { originalUrl: url, finalUrl: res.url }), finalUrl: res.url };
      if (last.state !== "error") {
        return { ...last, ms: Date.now() - startedAt };
      }
    } catch (error) {
      last = {
        ...classify(0, { error: error.name === "TimeoutError" ? "tiempo agotado" : error.message }),
        ms: Date.now() - startedAt,
      };
      if (error.name === "TimeoutError") return last;
    }
    if (attempt < retries) await new Promise((r) => setTimeout(r, RETRY_DELAY_MS));
  }
  return last;
}

/** Ejecuta las comprobaciones con un pool de concurrencia limitada. */
export async function checkAll(links, options = {}) {
  const { concurrency = DEFAULT_CONCURRENCY, timeoutMs = DEFAULT_TIMEOUT_MS } = options;
  const results = new Array(links.length);
  let cursor = 0;
  const workers = Array.from({ length: Math.min(concurrency, links.length) }, async () => {
    while (cursor < links.length) {
      const index = cursor;
      cursor += 1;
      const link = links[index];
      results[index] = { ...link, ...(await checkUrl(link.url, { timeoutMs })) };
    }
  });
  await Promise.all(workers);
  return results;
}

const SEVERITY = { caído: 0, error: 1, bloqueado: 2, redirige: 3, vivo: 4 };

/** Construye el informe en Markdown. */
export function buildReport(results, meta = {}) {
  const { files = [], date = new Date() } = meta;
  const counts = results.reduce((acc, r) => {
    acc[r.state] = (acc[r.state] || 0) + 1;
    return acc;
  }, {});
  const stamp = date.toISOString().slice(0, 10);
  const rows = [...results]
    .sort((a, b) => (SEVERITY[a.state] ?? 9) - (SEVERITY[b.state] ?? 9) || a.url.localeCompare(b.url))
    .map((r) => {
      const code = r.code ? String(r.code) : "—";
      const note = (r.note || "").replace(/\|/g, "\\|");
      return `| ${r.state} | ${code} | ${r.url} | ${note || "—"} |`;
    });

  return [
    `# Informe de enlaces — ${stamp}`,
    "",
    `Comprobación automática de **${results.length} enlaces** en ${files.map((f) => "`" + f + "`").join(", ")}.`,
    "Generado por `tools/check-links.mjs`. Un `bloqueado` no es un enlace muerto: es un sitio que rechaza bots y exige revisión manual.",
    "",
    `- **vivos**: ${counts.vivo || 0}`,
    `- **redirigen**: ${counts.redirige || 0}`,
    `- **bloqueados (revisar a mano)**: ${counts.bloqueado || 0}`,
    `- **caídos**: ${counts["caído"] || 0}`,
    `- **error / no concluyente**: ${counts.error || 0}`,
    "",
    "| Estado | Código | URL | Detalle |",
    "|---|---|---|---|",
    ...rows,
    "",
    `_Fecha de comprobación: ${stamp}. Volver a ejecutar con \`npm run check:links\`._`,
    "",
  ].join("\n");
}

/** Punto de entrada: lee ficheros, comprueba y escribe informe. */
export async function main(argv = process.argv.slice(2)) {
  const args = { files: [], out: "", json: false, strict: false, timeoutMs: DEFAULT_TIMEOUT_MS, concurrency: DEFAULT_CONCURRENCY };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === "--file") args.files.push(argv[++i]);
    else if (a === "--out") args.out = argv[++i];
    else if (a === "--json") args.json = true;
    else if (a === "--strict") args.strict = true;
    else if (a === "--timeout") args.timeoutMs = Number(argv[++i]);
    else if (a === "--concurrency") args.concurrency = Number(argv[++i]);
    else if (a === "--help" || a === "-h") {
      console.log("Uso: node tools/check-links.mjs [--file f.md]... [--out informe.md] [--json] [--strict] [--timeout ms] [--concurrency n]");
      return { results: [], exitCode: 0 };
    } else {
      throw new Error(`Argumento no reconocido: ${a}`);
    }
  }
  const files = args.files.length ? args.files : ["FUENTES.md"];

  const links = [];
  for (const file of files) {
    const markdown = await readFile(resolve(file), "utf8");
    links.push(...extractLinks(markdown).map((l) => ({ ...l, file })));
  }
  if (!links.length) throw new Error("No se ha encontrado ningún enlace en los ficheros dados.");

  const results = await checkAll(links, { concurrency: args.concurrency, timeoutMs: args.timeoutMs });
  const date = new Date();
  const out = args.out
    ? resolve(args.out)
    : resolve("INFORMES", `enlaces-${date.toISOString().slice(0, 10)}.md`);
  const report = buildReport(results, { files, date });
  await mkdir(dirname(out), { recursive: true });
  await writeFile(out, report, "utf8");

  if (args.json) {
    console.log(JSON.stringify({ results, report: out }, null, 2));
  } else {
    const counts = results.reduce((acc, r) => ({ ...acc, [r.state]: (acc[r.state] || 0) + 1 }), {});
    console.log(
      `Comprobados ${results.length} enlaces → vivos ${counts.vivo || 0} · redirigen ${counts.redirige || 0} · bloqueados ${counts.bloqueado || 0} · caídos ${counts["caído"] || 0} · error ${counts.error || 0}`,
    );
    console.log(`Informe: ${out}`);
    for (const r of results.filter((x) => x.state === "caído" || x.state === "redirige")) {
      console.log(`  ${r.state.toUpperCase()} ${r.code || ""} ${r.url}${r.note ? " — " + r.note : ""}`);
    }
  }

  const broken = results.filter((r) => r.state === "caído").length;
  return { results, report: out, exitCode: args.strict && broken > 0 ? 1 : 0 };
}

const isMain = process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  main()
    .then(({ exitCode }) => process.exit(exitCode))
    .catch((error) => {
      console.error(`check-links: ${error.message}`);
      process.exit(2);
    });
}
