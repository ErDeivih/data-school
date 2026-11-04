import pandas as pd

# Cada metrica declara hacia donde mejora y si es la norte o un guardarrail.
# Sin fijar esa direccion, un efecto positivo se lee como bueno aunque sea la latencia.
medidas = pd.DataFrame({
    "metrica": ["retencion_semana_4", "ingreso_por_usuario", "latencia_p95", "tickets_soporte"],
    "efecto": [0.018, 0.002, 0.150, 0.060],
    "limite_inferior": [0.004, -0.011, 0.040, 0.010],
    "limite_superior": [0.032, 0.015, 0.200, 0.110],
    "direccion": ["sube", "sube", "baja", "baja"],
    "norte": [True, False, False, False],
})

# Se orienta todo a "bueno" antes de leer: en las de direccion "baja" se cambia el signo.
signo = medidas.direccion.map({"sube": 1, "baja": -1})
inferior, superior = medidas.limite_inferior * signo, medidas.limite_superior * signo
medidas["lectura"] = "sin cambio"
medidas.loc[inferior > 0, "lectura"] = "mejora"
medidas.loc[superior < 0, "lectura"] = "empeora"
print(medidas[["metrica", "efecto", "direccion", "lectura"]].to_string(index=False))

norte_mejora = bool((medidas.loc[medidas.norte, "lectura"] == "mejora").all())
guardarrailes_ok = bool((medidas.loc[~medidas.norte, "lectura"] != "empeora").all())
print("la metrica norte mejora:", norte_mejora)               # -> True
print("los guardarrailes aguantan:", guardarrailes_ok)         # -> False
print("decision:", "lanzar" if norte_mejora and guardarrailes_ok
      else "no lanzar: la latencia se come la mejora")
