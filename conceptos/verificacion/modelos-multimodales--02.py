# El presupuesto de contexto de un sistema multimodal: una sola consulta, tres modalidades.
VENTANA = 128_000
MARGEN_SALIDA = 2_000          # reservado para la respuesta, no se toca

def consulta(imagenes, lado, texto_tokens, segundos_audio, vectores_por_segundo=50, troceado=16):
    import math
    n = math.ceil(lado / troceado)
    tokens_imagen = n * n * imagenes
    tokens_audio = segundos_audio * vectores_por_segundo
    total = tokens_imagen + tokens_audio + texto_tokens
    cabe = total + MARGEN_SALIDA <= VENTANA
    return tokens_imagen, tokens_audio, total, cabe

for caso, imagenes, lado, texto, segundos in (
    ("una factura", 1, 1008, 600, 0),
    ("diez facturas", 10, 448, 800, 0),
    ("factura y llamada de 10 min", 1, 672, 600, 600),
    ("reunion de una hora", 0, 0, 600, 3600),
):
    timg, taud, total, cabe = consulta(imagenes, lado, texto, segundos)
    print(f"{caso:30s} imagen {timg:6d}  audio {taud:6d}  total {total:7d}  "
          f"{'cabe' if cabe else 'NO CABE'}")
# -> una factura                    imagen   3969  audio      0  total    4569  cabe
# -> diez facturas                  imagen   7840  audio      0  total    8640  cabe
# -> factura y llamada de 10 min    imagen   1764  audio  30000  total   32364  cabe
# -> reunion de una hora            imagen      0  audio 180000  total  180600  NO CABE

# Cuanto de la ventana se come cada modalidad: es el numero que hay que graficar en produccion.
for caso, imagenes, lado, texto, segundos in (
    ("diez facturas", 10, 448, 800, 0),
    ("factura y llamada de 10 min", 1, 672, 600, 600),
):
    timg, taud, total, _ = consulta(imagenes, lado, texto, segundos)
    print(f"{caso:30s} imagen {timg / total:5.1%}  audio {taud / total:5.1%}  "
          f"texto {texto / total:5.1%}")
# -> diez facturas                  imagen 90.7%  audio  0.0%  texto  9.3%
# -> factura y llamada de 10 min    imagen  5.5%  audio 92.7%  texto  1.9%
