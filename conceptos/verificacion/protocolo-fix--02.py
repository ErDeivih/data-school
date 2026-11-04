SOH = "\x01"
mensaje = ("8=FIX.4.4" + SOH + "9=78" + SOH + "35=D" + SOH + "49=CLIENTE" + SOH +
           "56=BOLSA" + SOH + "34=7" + SOH + "11=ORD-1" + SOH + "55=BBVA" + SOH +
           "54=1" + SOH + "38=1000" + SOH + "40=2" + SOH + "44=9.85" + SOH +
           "59=0" + SOH + "10=168" + SOH)

campos = dict(campo.split("=", 1) for campo in mensaje.split(SOH) if campo)

# Se busca por numero de tag, nunca por posicion: el orden no esta garantizado
print(f"tipo de mensaje  {campos['35']}")        # -> D
print(f"simbolo          {campos['55']}")        # -> BBVA
print(f"lado             {campos['54']}")        # -> 1
print(f"cantidad         {campos['38']}")        # -> 1000
print(f"precio           {campos['44']}")        # -> 9.85
print(f"tags presentes   {len(campos)}")         # -> 14

# Comprobacion del checksum del propio mensaje: 93 bytes, suma 168 modulo 256
antes_del_checksum = mensaje[:mensaje.rindex("10=")]
print(f"checksum recalculado {sum(antes_del_checksum.encode('ascii')) % 256:03d}")  # -> 168
