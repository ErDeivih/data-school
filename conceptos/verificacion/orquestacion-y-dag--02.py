from datetime import datetime, timedelta

# Reintentos con espera exponencial: el fallo de red no deberia despertar a nadie.
base = timedelta(minutes=5)
t0 = datetime(2024, 3, 15, 3, 0)
minutos_extraccion = 35

for intento in range(1, 4):
    espera = base * (2 ** (intento - 1))
    print(f"reintento {intento}: espera {espera.seconds // 60} min")

espera_total = sum((base * (2 ** (k - 1))).seconds // 60 for k in range(1, 4))
print("espera acumulada:", espera_total, "min")     # -> espera acumulada: 35 min

# Tres intentos fallidos y el cuarto bueno, mas las esperas entre ellos.
fin_extraccion = t0 + timedelta(minutes=4 * minutos_extraccion + espera_total)
print("acaba la extraccion:", fin_extraccion.strftime("%H:%M"))   # -> acaba la extraccion: 05:55
print("acaba el DAG:", (fin_extraccion + timedelta(minutes=16)).strftime("%H:%M"))  # -> acaba el DAG: 06:11
