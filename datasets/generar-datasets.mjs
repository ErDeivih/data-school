// datos/generar-datasets.mjs — los seis datasets, deterministas y con manifiesto.
//
// Cada dataset se genera con una SEMILLA FIJA: los mismos bytes siempre, y por tanto el mismo SHA-256.
// Un dataset que no se puede regenerar con el mismo checksum no es un dataset, es un fichero con
// suerte. Y el manifiesto dice filas, columnas con su tipo y su unidad, licencia y checksum, para que
// el validador pueda comprobar que lo que se descarga es lo que se dice.
//
// Los datos son SINTÉTICOS: no salen de personas reales ni de fuentes con licencia dudosa. Eso se
// declara en cada uno.
//
//   node datos/generar-datasets.mjs

import { createHash } from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const RAIZ = process.cwd();
const SALIDA = join(RAIZ, "web", "datos", "datasets");
const MANIFIESTO = join(RAIZ, "web", "datos", "datasets.json");
mkdirSync(SALIDA, { recursive: true });

/** Generador pseudoaleatorio con semilla: mismo número siempre para la misma semilla y posición. */
function prng(semilla) {
  let a = semilla >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const conSigno = (r, escala) => Math.round((r() * 2 - 1) * escala * 1000) / 1000;
const entre = (r, a, b) => Math.round((a + r() * (b - a)) * 1000) / 1000;
const fecha = (dia) => new Date(Date.UTC(2026, 0, 1) + dia * 86400000).toISOString().slice(0, 10);

/** Los seis conjuntos: nombre, semilla, columnas con tipo y unidad, y cómo se genera cada fila. */
const CONJUNTOS = [
  {
    id: "ventas-mensuales",
    titulo: "Ventas mensuales por tienda",
    semilla: 20261001,
    filas: 180,
    descripcion: "Una serie de ventas diarias con estacionalidad semanal y una tendencia suave.",
    columnas: [
      { nombre: "fecha", tipo: "fecha", unidad: "ISO 8601" },
      { nombre: "tienda", tipo: "texto", unidad: "" },
      { nombre: "unidades", tipo: "entero", unidad: "uds" },
      { nombre: "ingresos", tipo: "decimal", unidad: "EUR" },
    ],
    genera: (r, k) => {
      const tendencia = 1 + k / 900;
      const semanal = 1 + 0.25 * Math.sin((k % 7) / 7 * Math.PI * 2);
      const unidades = Math.max(1, Math.round((60 + 25 * r()) * tendencia * semanal));
      const precio = 12 + 3 * r();
      return [fecha(k), ["centro", "norte", "sur"][k % 3], String(unidades), (unidades * precio).toFixed(2)];
    },
  },
  {
    id: "clientes-churn",
    titulo: "Clientes y baja",
    semilla: 20261002,
    filas: 200,
    descripcion: "Clientes sintéticos con antigüedad, uso mensual y si se dieron de baja.",
    columnas: [
      { nombre: "id_cliente", tipo: "texto", unidad: "" },
      { nombre: "antiguedad_meses", tipo: "entero", unidad: "meses" },
      { nombre: "uso_mensual", tipo: "entero", unidad: "sesiones" },
      { nombre: "reclamaciones", tipo: "entero", unidad: "uds" },
      { nombre: "baja", tipo: "booleano", unidad: "0/1" },
    ],
    genera: (r, k) => {
      const antig = Math.round(1 + r() * 47);
      const uso = Math.round(2 + r() * 40);
      const rec = Math.round(r() * 3);
      // La baja depende del uso y de las reclamaciones, no del azar puro: si no, no hay nada que aprender.
      const prob = Math.min(0.95, Math.max(0.02, 0.55 - uso * 0.012 + rec * 0.18 - antig * 0.004));
      return [`C${String(k + 1).padStart(4, "0")}`, String(antig), String(uso), String(rec), r() < prob ? "1" : "0"];
    },
  },
  {
    id: "precios-accion",
    titulo: "Precios diarios de una acción",
    semilla: 20261003,
    filas: 250,
    descripcion: "Paseo aleatorio con deriva, apertura, cierre, máximo, mínimo y volumen.",
    columnas: [
      { nombre: "fecha", tipo: "fecha", unidad: "ISO 8601" },
      { nombre: "apertura", tipo: "decimal", unidad: "EUR" },
      { nombre: "cierre", tipo: "decimal", unidad: "EUR" },
      { nombre: "maximo", tipo: "decimal", unidad: "EUR" },
      { nombre: "minimo", tipo: "decimal", unidad: "EUR" },
      { nombre: "volumen", tipo: "entero", unidad: "acciones" },
    ],
    genera: (r, k, estado) => {
      const previo = estado.cierre ?? 100;
      const cierre = Math.max(1, previo * (1 + conSigno(r, 0.02) / 1 + 0.0004));
      const apertura = previo;
      const maximo = Math.max(apertura, cierre) * (1 + Math.abs(conSigno(r, 0.008)));
      const minimo = Math.min(apertura, cierre) * (1 - Math.abs(conSigno(r, 0.008)));
      estado.cierre = cierre;
      return [fecha(k), apertura.toFixed(2), cierre.toFixed(2), maximo.toFixed(2), minimo.toFixed(2), String(Math.round(1e6 * (0.5 + r())))];
    },
  },
  {
    id: "sensores-planta",
    titulo: "Sensores de planta",
    semilla: 20261004,
    filas: 240,
    descripcion: "Lecturas de temperatura y presión con un episodio de avería.",
    columnas: [
      { nombre: "hora", tipo: "entero", unidad: "h desde el inicio" },
      { nombre: "temperatura", tipo: "decimal", unidad: "°C" },
      { nombre: "presion", tipo: "decimal", unidad: "bar" },
      { nombre: "estado", tipo: "texto", unidad: "" },
    ],
    genera: (r, k) => {
      const averia = k >= 150 && k < 168;
      const temp = (70 + 6 * Math.sin(k / 12) + conSigno(r, 1.2)) + (averia ? 18 : 0);
      const pres = (4 + 0.4 * Math.sin(k / 9) + conSigno(r, 0.08)) + (averia ? 1.6 : 0);
      return [String(k), temp.toFixed(2), pres.toFixed(2), averia ? "averia" : (k % 24 < 8 ? "parada" : "marcha")];
    },
  },
  {
    id: "encuestas-satisfaccion",
    titulo: "Encuestas de satisfacción",
    semilla: 20261005,
    filas: 160,
    descripcion: "Puntuaciones de 0 a 10 por segmento, con una cola de insatisfechos.",
    columnas: [
      { nombre: "id", tipo: "texto", unidad: "" },
      { nombre: "segmento", tipo: "texto", unidad: "" },
      { nombre: "puntuacion", tipo: "entero", unidad: "0-10" },
      { nombre: "recomienda", tipo: "booleano", unidad: "0/1" },
    ],
    genera: (r, k) => {
      const seg = ["nuevo", "habitual", "veterano"][k % 3];
      const base = seg === "veterano" ? 2.2 : seg === "habitual" ? 1.3 : 0;
      const p = Math.min(10, Math.max(0, Math.round(base + r() * 9 - (r() < 0.12 ? 5 : 0))));
      return [`E${String(k + 1).padStart(4, "0")}`, seg, String(p), p >= 9 ? "1" : "0"];
    },
  },
  {
    id: "algoritmos-tiempos",
    titulo: "Tiempos de algoritmos",
    semilla: 20261006,
    filas: 180,
    descripcion: "Tiempo de ejecución de seis algoritmos de ordenación con tamaños crecientes.",
    columnas: [
      { nombre: "algoritmo", tipo: "texto", unidad: "" },
      { nombre: "n", tipo: "entero", unidad: "elementos" },
      { nombre: "milisegundos", tipo: "decimal", unidad: "ms" },
    ],
    genera: (r, k) => {
      const alg = ["burbuja", "insercion", "seleccion", "mezcla", "rapido", "monticulo"][k % 6];
      const n = 100 * (1 + Math.floor(k / 6));
      const coste = { burbuja: n * n, insercion: n * n * 0.6, seleccion: n * n * 0.8, mezcla: n * Math.log2(n), rapido: n * Math.log2(n) * 0.8, monticulo: n * Math.log2(n) * 1.2 }[alg];
      return [alg, String(n), (coste / 90000 * (0.9 + r() * 0.2)).toFixed(3)];
    },
  },
  {
    id: "telemetria-f1",
    titulo: "Telemetria de una carrera",
    semilla: 20261101,
    filas: 180,
    descripcion: "Tres carreras, dos pilotos y treinta vueltas por piloto, con compuesto, desgaste y una parada por piloto y carrera.",
    columnas: [
      { nombre: "carrera", tipo: "texto", unidad: "" },
      { nombre: "piloto", tipo: "texto", unidad: "" },
      { nombre: "vuelta", tipo: "entero", unidad: "vueltas" },
      { nombre: "compuesto", tipo: "texto", unidad: "" },
      { nombre: "edad_neumatico", tipo: "entero", unidad: "vueltas" },
      { nombre: "sector1_s", tipo: "decimal", unidad: "s" },
      { nombre: "sector2_s", tipo: "decimal", unidad: "s" },
      { nombre: "sector3_s", tipo: "decimal", unidad: "s" },
      { nombre: "tiempo_vuelta_s", tipo: "decimal", unidad: "s" },
      { nombre: "parada", tipo: "booleano", unidad: "0/1" },
    ],
    genera: (r, k) => {
      const carreras = ["bahrein", "monza", "suzuka"];
      const c = Math.floor(k / 60);
      const dentro = k % 60;
      const piloto = dentro < 30 ? "A" : "B";
      const vuelta = (dentro % 30) + 1;
      const paradaEn = piloto === "A" ? 18 : 22;
      const parada = vuelta === paradaEn ? 1 : 0;
      const edad = vuelta <= paradaEn ? vuelta : vuelta - paradaEn;
      const compuesto = vuelta <= paradaEn ? "medio" : "duro";
      const base = { bahrein: 92.5, monza: 84.2, suzuka: 91.1 }[carreras[c]];
      const degradacion = 0.055 * edad + (compuesto === "duro" ? -0.25 : 0);
      const combustible = -0.03 * vuelta;
      const vueltaS = base + degradacion + combustible + (parada ? 22.4 : 0) + conSigno(r, 0.35);
      const s1 = vueltaS * 0.33 + conSigno(r, 0.08);
      const s2 = vueltaS * 0.34 + conSigno(r, 0.08);
      const s3 = vueltaS - s1 - s2;
      return [carreras[c], piloto, String(vuelta), compuesto, String(edad),
              s1.toFixed(3), s2.toFixed(3), s3.toFixed(3), vueltaS.toFixed(3), String(parada)];
    },
  },
  {
    id: "cartera-acciones",
    titulo: "Cartera de acciones frente a un indice",
    semilla: 20261102,
    filas: 360,
    descripcion: "Sesenta meses de retornos de cinco acciones y un indice, con un factor de mercado comun y ruido propio.",
    columnas: [
      { nombre: "mes", tipo: "fecha", unidad: "ISO 8601" },
      { nombre: "activo", tipo: "texto", unidad: "" },
      { nombre: "retorno", tipo: "decimal", unidad: "tanto por uno" },
    ],
    genera: (r, k) => {
      const activos = ["indice", "accion-a", "accion-b", "accion-c", "accion-d", "accion-e"];
      const a = k % 6;
      const mes = Math.floor(k / 6);
      const comun = conSigno(r, 0.035);
      const beta = [1, 1.1, 0.9, 1.4, 0.6, 1.25][a];
      const idio = conSigno(r, 0.02 + 0.015 * a);
      const valor = a === 0 ? comun : beta * comun + idio;
      const fechaMes = new Date(Date.UTC(2021, mes, 1)).toISOString().slice(0, 10);
      return [fechaMes, activos[a], valor.toFixed(5)];
    },
  },
  {
    id: "f1-clasificacion",
    titulo: "Clasificacion y carrera de F1",
    semilla: 20261103,
    filas: 400,
    descripcion: "Veinte carreras con veinte pilotos: tiempos de clasificacion, compuesto, temperatura y posicion final.",
    columnas: [
      { nombre: "carrera", tipo: "texto", unidad: "" },
      { nombre: "piloto", tipo: "texto", unidad: "" },
      { nombre: "equipo", tipo: "texto", unidad: "" },
      { nombre: "posicion_quali", tipo: "entero", unidad: "puesto" },
      { nombre: "vuelta_quali_s", tipo: "decimal", unidad: "s" },
      { nombre: "sector1_s", tipo: "decimal", unidad: "s" },
      { nombre: "sector2_s", tipo: "decimal", unidad: "s" },
      { nombre: "sector3_s", tipo: "decimal", unidad: "s" },
      { nombre: "compuesto", tipo: "texto", unidad: "" },
      { nombre: "temperatura_c", tipo: "decimal", unidad: "C" },
      { nombre: "posicion_final", tipo: "entero", unidad: "puesto" },
      { nombre: "puntos", tipo: "entero", unidad: "puntos" },
    ],
    genera: (r, k, estado) => {
      const equipos = ["alfa", "beta", "gamma", "delta", "epsilon"];
      if (k % 20 === 0) {
        // Una carrera completa de golpe: hace falta ordenar los 20 tiempos para asignar puestos.
        const filas = [];
        for (let i = 0; i < 20; i++) {
          const piloto = "P" + String(i + 1).padStart(2, "0");
          const equipo = equipos[Math.floor(i / 4)];
          const coche = { alfa: 0.35, beta: 0.20, gamma: 0.05, delta: -0.10, epsilon: -0.25 }[equipo];
          const habilidad = 0.30 * Math.cos(i * 0.7) - i * 0.012;
          const temperatura = 24 + 8 * r();
          const compuesto = r() < 0.5 ? "blando" : "medio";
          const vuelta = 88.0 - coche - habilidad + conSigno(r, 0.30) + (compuesto === "blando" ? -0.15 : 0) + (temperatura > 30 ? 0.12 : 0);
          filas.push({ piloto, equipo, vuelta, compuesto, temperatura });
        }
        filas.sort((a, b) => a.vuelta - b.vuelta);
        estado.carrera = filas.map((f, pos) => {
          const s1 = f.vuelta * 0.32 + conSigno(r, 0.05);
          const s2 = f.vuelta * 0.36 + conSigno(r, 0.05);
          const final = Math.min(20, Math.max(1, pos + 1 + Math.round(conSigno(r, 2.2))));
          const puntos = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1];
          return { ...f, pos: pos + 1, s1, s2, final, puntos: final <= 10 ? puntos[final - 1] : 0 };
        });
      }
      const d = estado.carrera[k % 20];
      const s3 = d.vuelta - d.s1 - d.s2;
      return ["r" + String(Math.floor(k / 20) + 1).padStart(2, "0"), d.piloto, d.equipo, String(d.pos),
              d.vuelta.toFixed(3), d.s1.toFixed(3), d.s2.toFixed(3), s3.toFixed(3),
              d.compuesto, d.temperatura.toFixed(1), String(d.final), String(d.puntos)];
    },
  },
  {
    id: "futbol-partidos",
    titulo: "Partidos de liga con tiros y xG",
    semilla: 20261104,
    filas: 380,
    descripcion: "Una liga de veinte equipos: goles, tiros, xG, posesion y tarjetas por partido.",
    columnas: [
      { nombre: "jornada", tipo: "entero", unidad: "jornada" },
      { nombre: "local", tipo: "texto", unidad: "" },
      { nombre: "visitante", tipo: "texto", unidad: "" },
      { nombre: "goles_local", tipo: "entero", unidad: "goles" },
      { nombre: "goles_visitante", tipo: "entero", unidad: "goles" },
      { nombre: "tiros_local", tipo: "entero", unidad: "tiros" },
      { nombre: "tiros_visitante", tipo: "entero", unidad: "tiros" },
      { nombre: "xg_local", tipo: "decimal", unidad: "goles esperados" },
      { nombre: "xg_visitante", tipo: "decimal", unidad: "goles esperados" },
      { nombre: "posesion_local", tipo: "entero", unidad: "%" },
      { nombre: "amarillas", tipo: "entero", unidad: "tarjetas" },
      { nombre: "resultado", tipo: "texto", unidad: "1 X 2" },
    ],
    genera: (r, k) => {
      const equipos = Array.from({ length: 20 }, (_, i) => "equipo-" + String(i + 1).padStart(2, "0"));
      const fuerza = (i) => 1.6 - i * 0.06;
      const local = k % 20;
      const visitante = (k * 7 + 3) % 20;
      const ataque = (fuerza(local) + 0.25) * (0.75 + 0.5 * r());
      const defensa = (fuerza(visitante)) * (0.75 + 0.5 * r());
      const xgL = Math.max(0.15, ataque * 1.15 - defensa * 0.35);
      const xgV = Math.max(0.10, defensa * 0.95 - ataque * 0.20);
      const goles = (x) => Math.max(0, Math.round(x + conSigno(r, 1.05)));
      const gl = goles(xgL);
      const gv = goles(xgV);
      const tirosL = Math.max(2, Math.round(xgL * 9 + conSigno(r, 2.5)));
      const tirosV = Math.max(2, Math.round(xgV * 9 + conSigno(r, 2.5)));
      const posesion = Math.min(75, Math.max(25, Math.round(50 + (xgL - xgV) * 12 + conSigno(r, 4))));
      return [String(Math.floor(k / 10) + 1), equipos[local], equipos[visitante], String(gl), String(gv),
              String(tirosL), String(tirosV), xgL.toFixed(2), xgV.toFixed(2), String(posesion),
              String(Math.round(r() * 6)), gl > gv ? "1" : gl === gv ? "X" : "2"];
    },
  },
];

function csvDe(columnas, filas) {
  const cabeza = columnas.map((c) => c.nombre).join(",");
  return [cabeza, ...filas.map((f) => f.join(","))].join("\n") + "\n";
}

const manifiesto = { version: 1, generadoPor: "datos/generar-datasets.mjs", semilla: "fija por conjunto", licencia: "CC0-1.0 (datos sinteticos)", conjuntos: [] };
for (const c of CONJUNTOS) {
  const r = prng(c.semilla);
  const estado = {};
  const filas = [];
  for (let k = 0; k < c.filas; k++) filas.push(c.genera(r, k, estado));
  const texto = csvDe(c.columnas, filas);
  const fichero = c.id + ".csv";
  writeFileSync(join(SALIDA, fichero), texto, "utf8");
  const checksum = createHash("sha256").update(texto, "utf8").digest("hex");
  manifiesto.conjuntos.push({
    id: c.id,
    titulo: c.titulo,
    fichero: "datos/datasets/" + fichero,
    filas: filas.length,
    columnas: c.columnas,
    descripcion: c.descripcion,
    origen: "sintetico",
    licencia: "CC0-1.0",
    checksum: "sha256:" + checksum,
  });
  console.log(`  ${c.id}: ${filas.length} filas · sha256:${checksum.slice(0, 12)}…`);
}
writeFileSync(MANIFIESTO, JSON.stringify(manifiesto, null, 1) + "\n", "utf8");
console.log(`\n  manifiesto: web/datos/datasets.json con ${manifiesto.conjuntos.length} conjuntos`);
