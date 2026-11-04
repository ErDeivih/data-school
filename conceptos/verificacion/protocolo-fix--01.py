SOH = "\x01"

def fix(campos):
    """Monta un mensaje FIX: longitud de cuerpo y checksum calculados de verdad."""
    cuerpo = "".join(f"{t}={v}{SOH}" for t, v in campos)
    sin_checksum = f"8=FIX.4.4{SOH}9={len(cuerpo)}{SOH}" + cuerpo
    checksum = sum(sin_checksum.encode("ascii")) % 256
    return sin_checksum + f"10={checksum:03d}{SOH}"

msg = fix([(35, "D"), (49, "CLIENTE"), (56, "BOLSA"), (34, 7), (11, "ORD-1"),
           (55, "BBVA"), (54, 1), (38, 1000), (40, 2), (44, "9.85"), (59, 0)])

print(f"bytes totales   {len(msg)}")             # -> 100
print(f"body length     {msg.split(SOH)[1]}")   # -> 9=78
print(f"checksum        {msg[-4:-1]}")          # -> 168
print(msg.replace(SOH, "|"))                     # -> 8=FIX.4.4|9=78|35=D|49=CLIENTE|56=BOLSA|34=7|11=ORD-1|55=BBVA|54=1|38=1000|40=2|44=9.85|59=0|10=168|
