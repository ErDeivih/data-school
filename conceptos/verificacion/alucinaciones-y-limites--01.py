import re

contexto = ("Las devoluciones se admiten dentro de los 14 dias naturales desde la entrega. "
            "Para productos personalizados el plazo es de 7 dias. El reembolso se emite "
            "en un maximo de 5 dias laborables tras la recepcion.")

respuestas = [
    "Tienes 14 dias naturales desde la entrega.",
    "Tienes 30 dias naturales segun la normativa europea.",
    "Tienes 14 dias, o 10 si el producto es personalizado.",
]

# set() de todos los numeros de la fuente: la comprobacion es por coincidencia exacta
numeros_contexto = set(re.findall(r"\d+", contexto))

for r in respuestas:
    # \d+ encuentra cada numero de la respuesta; findall devuelve texto, no enteros
    numeros = re.findall(r"\d+", r)
    # el anclaje se mide numero a numero: los que no estan en la fuente se cuentan aparte
    anclados = [n for n in numeros if n in numeros_contexto]
    # exigir TODOS anclados es lo que rechaza la respuesta 3, la mas peligrosa
    fiel = len(anclados) == len(numeros)
    print(f"anclaje {len(anclados)}/{len(numeros)}  fiel {fiel}  {r[:40]}")
# solo la primera usa exclusivamente numeros que estan en el contexto
