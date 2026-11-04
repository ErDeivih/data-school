import json
import re

# Por que no se parsea texto libre: la misma peticion, cinco variantes del mismo dato.
crudo = [
    '{"importe": 1250.0, "moneda": "EUR"}',
    '{"importe": 1250.0, "moneda": "EUR",}',
    'El resultado es {"importe": 1250.0, "moneda": "EUR"} y nada mas.',
    "```json\n{\"importe\": 1250.0, \"moneda\": \"EUR\"}\n```",
    "Aqui lo tienes: {'importe': 1250.0, 'moneda': 'EUR'}",
]

patron = re.compile(r'"importe"\s*:\s*([0-9.]+)')   # los parentesis capturan el numero como TEXTO

for texto in crudo:
    # quita las vallas de codigo, pero solo las de los extremos: el ^ y el $ lo limitan
    limpio = re.sub(r"^```(?:json)?\s*|\s*```$", "", texto.strip())
    try:
        dato = json.loads(limpio)
        print("json.loads ok     ", dato)
    except json.JSONDecodeError as error:
        # error.pos es la posicion del caracter donde el parser se ha atascado
        print("json.loads falla  ", error.msg, "en la posicion", error.pos)

    coincidencia = patron.search(texto)             # search devuelve un Match, o None si no hay nada
    print("   regex ve         ", coincidencia.group(1) if coincidencia else "nada")
# la regex acierta cuatro veces y falla en la ultima: comillas simples y sin comillas dobles
