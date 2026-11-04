import hashlib

def pseudo(valor, sal=""):
    # Un hash truncado a 12 caracteres basta como alias, pero no protege nada por si solo.
    return hashlib.sha256((sal + valor).encode()).hexdigest()[:12]

# Un identificador de 5 digitos tiene 90.000 valores: se enumeran todos.
objetivo = pseudo("34521")
recuperado = next(v for v in range(10_000, 100_000) if pseudo(str(v)) == objetivo)
print("recuperado del hash sin sal:", recuperado)     # -> recuperado del hash sin sal: 34521

# Con sal secreta el mismo valor produce otro hash, y la sal no puede vivir con los datos.
print("mismo valor con sal:", pseudo("34521", sal="s3cr3t0-a1"))   # -> mismo valor con sal: 72ceabaf4ad3
