# Lo que se guarda de una traza: la lista de spans con sus atributos, que es lo que hace
# reproducible un fallo. Sin esto, la misma pregunta da respuestas distintas y no hay caso.
import json

TRAZA = {
    "trace_id": "3f9a1c",
    "consulta": "cuanto tarda el pedido A-4471",
    "version": {"modelo": "abierto-8b-v3", "prompt": "soporte-12", "indice": "docs-2026-10-01"},
    "spans": [
        {"nombre": "recuperar", "ms": 42, "atributos": {"documentos": 3, "tokens": 1260}},
        {"nombre": "modelo", "ms": 1180, "atributos": {"tokens_entrada": 3180,
                                                       "tokens_cache": 1200,
                                                       "tokens_salida": 246}},
        {"nombre": "validar", "ms": 3, "atributos": {"esquema": "respuesta_v2", "valido": True}},
        {"nombre": "reenviar", "ms": 1840, "atributos": {"motivo": "timeout del proveedor"}},
        {"nombre": "modelo", "ms": 1090, "atributos": {"tokens_entrada": 3180,
                                                       "tokens_cache": 1200,
                                                       "tokens_salida": 252}},
    ],
}

P_ENTRADA, P_CACHE, P_SALIDA = 3.00, 0.30, 15.00

def resumen(traza):
    coste = 0.0
    for span in traza["spans"]:
        a = span["atributos"]
        if span["nombre"] == "modelo":
            coste += (a["tokens_entrada"] * P_ENTRADA + a["tokens_cache"] * P_CACHE
                      + a["tokens_salida"] * P_SALIDA) / 1e6
    return {"span_mas_lento": max(traza["spans"], key=lambda s: s["ms"])["nombre"],
            "ms_total": sum(s["ms"] for s in traza["spans"]),
            "llamadas_al_modelo": sum(1 for s in traza["spans"] if s["nombre"] == "modelo"),
            "coste": round(coste, 6)}

resumen_traza = resumen(TRAZA)
print(json.dumps(resumen_traza, ensure_ascii=True, sort_keys=True))
# -> {"coste": 0.02727, "llamadas_al_modelo": 2, "ms_total": 4155, "span_mas_lento": "reenviar"}

# El span mas caro no es el mas lento: por eso hacen falta las dos metricas, no una.
for span in TRAZA["spans"]:
    print(f"{span['nombre']:10s} {span['ms']:5d} ms")
# -> recuperar     42 ms
# -> modelo      1180 ms
# -> validar        3 ms
# -> reenviar    1840 ms
# -> modelo      1090 ms
