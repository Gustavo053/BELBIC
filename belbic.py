import calc

# initial values
alpha = 0.45
beta = 0.01

kp = 3.98
ki = 0.58
kd = 0.63

h = 0.01

iMax = 3.3


def SI(e, eant, iant):
    # print(f'eant: ', eant)
    # print(f'iant: ', iant)
    global h
    
    P = e * kp
    I = iant + (ki * h) * (e + eant)
    D = (kd/h) * (e - eant)

    if (I > iMax):
        I = iMax
    elif (I <= 0):
        I = 0

    dedt = (e - eant)/h
    si = P + I + D

    # print(f'SI: ', si)
    # print(f'dedt: ', dedt)

    return si, dedt, e, I


def thalamus(sensors_input):
    Ath = calc.Ath(sensors_input)
    print(f'Ath: ', Ath)
    print(f'sensors_input', sensors_input)

    return sensors_input, Ath


def sensory_cortex(sensors_input, rew, A, E_dot, vi, wi):
    global alpha
    global beta

    viNew = calc.delta_vi(alpha, sensors_input, rew, A) + vi
    wiNew = calc.delta_wi(beta, sensors_input, rew, E_dot) + wi

    return viNew, wiNew


def orbifrontal_cortex(wi, sensors_input, A, O, rew):
    O = calc.Ot(wi, sensors_input)
    E_dot = calc.e_dot(A, O) * rew

    return O, E_dot


def amygdala(vi, sensors_input, A, O, rew):
    # A.append(Ath)

    A = calc.Am(vi, sensors_input)
    E = calc.e(A, O) * rew

    return A, E


def run(alpha, beta):
    return None
