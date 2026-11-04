import re

texto = "Pedido 2024-03-05 entregado, factura 2024-04-12 pendiente"

# Grupos con nombre: se leen por su significado y no por su posicion.
FECHA = re.compile(r"(?P<anio>\d{4})-(?P<mes>\d{2})-(?P<dia>\d{2})")
print(" ".join(f"{m['dia']}/{m['mes']}/{m['anio']}" for m in FECHA.finditer(texto)))
# -> 05/03/2024 12/04/2024

# El asterisco es codicioso: se estira hasta el ultimo cierre. Con el interrogante, no.
print(re.search(r"<b>.*</b>", "a <b>uno</b> y <b>dos</b>").group(0))
# -> <b>uno</b> y <b>dos</b>
print(re.search(r"<b>.*?</b>", "a <b>uno</b> y <b>dos</b>").group(0))
# -> <b>uno</b>

# Lookahead: exigir un digito en cualquier posicion sin consumir caracteres.
print(bool(re.fullmatch(r"(?=.*\d)[A-Za-z0-9]{6,}", "abc123")))   # -> True
print(bool(re.fullmatch(r"(?=.*\d)[A-Za-z0-9]{6,}", "abcdef")))   # -> False
