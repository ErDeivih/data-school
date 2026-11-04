import re

# Minimizar antes de enviar: quitar identificadores directos del texto.
ticket = "Soy Ana Ruiz (ana.ruiz@ejemplo.es), pedido 4471, no me llega el pedido."

def minimizar(texto):
    # El correo se sustituye sin comerse los parentesis que lo rodean.
    # [^\s()] es "todo menos espacio o parentesis"; re.sub devuelve una cadena NUEVA, no toca texto
    sin_correo = re.sub(r"[^\s()]+@[^\s()]+", "[correo]", texto)
    # depende de tres cosas a la vez: la palabra "Soy", las mayusculas y un nombre de dos palabras
    sin_nombre = re.sub(r"Soy [A-Z][a-z]+ [A-Z][a-z]+", "Soy [cliente]", sin_correo)
    # \d+ es "uno o mas digitos": solo cae el numero que va detras de la palabra pedido
    return re.sub(r"pedido \d+", "pedido [ref]", sin_nombre)

limpio = minimizar(ticket)                       # el original sigue intacto: se trabaja sobre copias
print(limpio)
# -> Soy [cliente] ([correo]), pedido [ref], no me llega el pedido.
# len cuenta CARACTERES, no tokens: la rebaja de 71 a 62 no mide el riesgo que se quita
print("caracteres originales:", len(ticket))     # -> 71
print("caracteres enviados  :", len(limpio))     # -> 62
