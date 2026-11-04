# Que se despierta a las cuatro de la manana depende de la gravedad, no de lo interesante
# que sea el fallo. Las reglas se escriben ANTES, para no discutirlas con el sistema caido.
ESCALADO = {
    #         a quien se avisa        comunicacion  plazo de escalada
    "SEV1": ("guardia + responsable", "30 min", "15 min"),
    "SEV2": ("guardia",               "1 h",    "1 h"),
    "SEV3": ("horario laboral",       "fin de dia", "no"),
    "SEV4": ("tarea",                 "no",     "no"),
}

def clasificar(servicio_principal, usuarios_afectados, hay_perdida_de_datos):
    # El orden de las comprobaciones importa: la primera condicion que se cumple manda.
    if servicio_principal or hay_perdida_de_datos:
        return "SEV1"
    if usuarios_afectados >= 100:
        return "SEV2"
    if usuarios_afectados > 0:
        return "SEV3"
    return "SEV4"

casos = [
    ("pagos caido", True, 5000, False),
    ("informes lentos", False, 300, False),
    ("un cliente sin acceso", False, 1, False),
    ("error de datos corregido", False, 0, True),
]
for nombre, principal, usuarios, datos in casos:
    sev = clasificar(principal, usuarios, datos)
    a_quien, cada, plazo = ESCALADO[sev]
    print(f"{nombre:28} {sev}  avisar: {a_quien:22} cada {cada}")
