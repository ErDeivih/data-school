# Cada instruccion del Dockerfile es una capa cacheada. Cambiar una capa obliga a
# rehacer esa y todas las posteriores; las anteriores se reutilizan.
def segundos_rehechos(capas, coste, capa_tocada):
    return sum(coste[c] for c in capas[capas.index(capa_tocada):])

coste = {
    "FROM python:3.12-slim": 2,
    "COPY requirements.txt": 0,
    "RUN pip install -r requirements.txt": 45,
    "COPY . /app": 0,
}

malo = ["FROM python:3.12-slim", "COPY . /app", "RUN pip install -r requirements.txt"]
bueno = ["FROM python:3.12-slim", "COPY requirements.txt",
         "RUN pip install -r requirements.txt", "COPY . /app"]

# Tocas un fichero .py: la unica capa que cambia de contenido es el COPY del codigo
print("mal orden: ", segundos_rehechos(malo, coste, "COPY . /app"), "s")   # -> 45 s
print("buen orden:", segundos_rehechos(bueno, coste, "COPY . /app"), "s")  # -> 0 s
