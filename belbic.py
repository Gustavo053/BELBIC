import calc

# initial values
alpha = 6
beta = 9
rew = 4

Ath = 0
E_dot = 0
E = 0

O = []
A = []

sensors_input = [0]


def thalamus(sensors_input):
    global Ath
    Ath = calc.Ath(sensors_input)
    print(f'Ath: ', Ath)
    print(f'sensors_input', sensors_input)

    return sensors_input, Ath


def sensory_cortex(sensors_input):
    vi = calc.delta_vi(alpha, sensors_input, rew, A)
    wi = calc.delta_wi(beta, sensors_input, rew)

    return vi, wi


def orbifrontal_cortex(wi, sensors_input, rew):
    global O
    global E_dot

    O = calc.Ot(wi, sensors_input)
    E_dot = calc.e_dot(A, O) * rew

    return O, E_dot


def amygdala(Ath, vi, sensors_input, rew):
    global A
    global E

    A.append(Ath)

    A = calc.Am(vi, sensors_input)
    E = calc.e(A, O) * rew

    return A, E
