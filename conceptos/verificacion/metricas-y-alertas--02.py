# --- inicio formula 2 ---
# El burn rate decide si una alerta es un incendio o una deriva. Mismo SLO, traficos distintos.
def burn_rate(tasa_de_error, slo):
    # Cuantas veces mas rapido se gasta el presupuesto que al ritmo permitido.
    return tasa_de_error / (1 - slo)

casos = [
    ("pico de 5 minutos al 4 %", 0.04, 5),
    ("incidente de 40 minutos al 4 %", 0.04, 40),
    ("incidente de 6 horas al 4 %", 0.04, 360),
    ("deriva del 0,15 % todo el mes", 0.0015, 43200),
]
ventana_minutos = 30 * 24 * 60

for nombre, tasa, minutos in casos:
    br = burn_rate(tasa, 0.999)
    # Lo gastado es el burn rate por la fraccion de la ventana que duro el fallo: quemar al
    # cuadruple durante una hora de un mes de 720 horas gasta 4/720 del presupuesto.
    consumido = br * minutos / ventana_minutos
    # El presupuesto no se puede gastar dos veces: al 100 % esta agotado y el resto es dano
    # que ya no cabe. El burn rate baja a 1 cuando se topa, no sigue subiendo.
    print("%-32s burn %5.1f  presupuesto %6.2f%%  se agota en %s"
          % (nombre, br, 100 * consumido,
             "no aplica" if br <= 1 else "%.0f h" % (ventana_minutos / br / 60)))
# --- fin formula 2 ---
# -> pico de 5 minutos al 4 %        burn  40.0  presupuesto   0.46%  se agota en  18 h
# -> incidente de 40 minutos al 4 %  burn  40.0  presupuesto   3.70%  se agota en  18 h
# -> incidente de 6 horas al 4 %     burn  40.0  presupuesto  33.33%  se agota en  18 h
# -> deriva del 0,15 % todo el mes   burn   1.5  presupuesto 150.00%  se agota en 480 h
# Ojo: el burn rate es el MISMO en los tres primeros casos porque la tasa de error es la misma.
# Lo que cambia el dano no es el burn rate, es cuanto tiempo se sostiene. La deriva es al reves:
# un burn rate modesto (1,5) que dura el mes entero agota el presupuesto en 20 dias, y eso no lo
# detecta ninguna alerta de incendio.
