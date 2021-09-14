import calc

# initial values
alpha = 0
beta = 0
rew = 0

Ath = 0
E_dot = 0
E = 0

O = []
A = []

sensors_input = 0

kp = 3.84  # 3.84
ki = 1.39  # 1.39
kd = 2.0  # 2.00

h = 0.01

u = 0

# erro inicial
eant = 0
# parte integrativa inicial
iant = 0

iMax = 5
uMax = 5


def SI(e, tMax):
    P = e * kp
    I = iant + (ki * h) * (e + eant)
    D = (kd/h) * (e - eant)

    if (I > iMax):
        I = iMax
    elif (I <= 0):
        I = 0

    dedt = (e - eant)/h
    si = P + I + D

    return si, dedt


def thalamus(sensors_input):
    global Ath
    Ath = calc.Ath(sensors_input)
    print(f'Ath: ', Ath)
    print(f'sensors_input', sensors_input)

    return sensors_input, Ath


def sensory_cortex(sensors_input):
    vi = calc.delta_vi(alpha, sensors_input, rew, A)
    wi = calc.delta_wi(beta, sensors_input, rew, E_dot)

    return vi, wi


def orbifrontal_cortex(wi, sensors_input, rew):
    global O
    global E_dot

    O = calc.Ot(wi, sensors_input)
    E_dot = calc.e_dot(A, O) * rew

    return O, E_dot


def amygdala(vi, sensors_input, rew):
    global A
    global E

    # A.append(Ath)

    A = calc.Am(vi, sensors_input)
    E = calc.e(A, O) * rew

    return A, E


def run(alpha, beta):
    return None
