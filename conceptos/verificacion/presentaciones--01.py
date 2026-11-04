# Cuanto material cabe: una persona lee unas 140 palabras por minuto de discurso.
# Lo que no cabe en el guion no se cuenta, y lo que no se cuenta sobra en la diapositiva.
palabras_por_minuto = 140
minutos_contenido = 12          # 15 asignados menos 3 reservados para preguntas

for diapositivas in (20, 12, 8):
    segundos = minutos_contenido * 60 / diapositivas
    palabras = minutos_contenido * palabras_por_minuto / diapositivas
    print(f"{diapositivas:>2} diapositivas en {minutos_contenido} min -> "
          f"{segundos:.0f} s y {palabras:.0f} palabras por diapositiva")
# -> 20 diapositivas en 12 min -> 36 s y 84 palabras por diapositiva
# -> 12 diapositivas en 12 min -> 60 s y 140 palabras por diapositiva
# ->  8 diapositivas en 12 min -> 90 s y 210 palabras por diapositiva
