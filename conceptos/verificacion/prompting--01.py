# Montar un prompt y comprobar que cabe: contar caracteres es una aproximacion,
# el numero real de tokens lo da el tokenizador del modelo.
sistema = "Eres un asistente que responde en espanol de Espana, breve y sin relleno."
documentos = [
    "El contrato se renueva automaticamente cada 12 meses salvo aviso con 30 dias.",
    "La facturacion se emite el primer dia laborable de cada mes.",
    "El soporte responde en un maximo de 8 horas laborables.",
]
pregunta = "Cuando puedo cancelar sin penalizacion?"

partes = [f"[SISTEMA] {sistema}"]
for i, d in enumerate(documentos, 1):        # enumerate empieza en 1: los documentos se numeran [DOC 1], [DOC 2]...
    partes.append(f"[DOC {i}] {d}")
partes.append(f"[PREGUNTA] {pregunta}")
partes.append("[FORMATO] Responde solo con la fecha o el plazo, sin explicaciones.")

prompt = "\n".join(partes)                   # une las piezas con salto de linea: los delimitadores van dentro
caracteres = len(prompt)                     # cuenta caracteres, NO tokens: es la aproximacion que se critica
print(f"caracteres {caracteres}  tokens aproximados {caracteres // 4}")     # -> 421  105
print(f"peor caso (2 caracteres por token) {caracteres // 2} tokens")      # -> 210
