def Ath(sensors):
    bigger = max(sensors)
    return bigger


def delta_vi(alpha, sensors_input, rew):
    v = []

    for si in sensors_input:
        v.append(alpha * (si * rew))

    return v


def delta_wi(beta, sensors_input, rew):
    w = []

    for si in sensors_input:
        w.append(beta * (si * rew))

    return w


def e(A, O):
    sum_a = 0
    sum_o = 0
    result_e = 0
    for i in vi:
        sum_a = sum_a + i

    for j in wi:
        sum_o = sum_o + j

    result_e = sum_a - sum_o

    return result_e


def e_dot(A, O):
    sum_a = 0
    sum_o = 0
    result_e_dot = 0
    for i in vi:
        sum_a = sum_a + i

    for j in wi:
        sum_o = sum_o + j

    result_e_dot = sum_a - sum_o

    return result_e_dot


def Ot(wi, si):
    result_ot = []

    for i in range(len(wi)):
        result_ot.append(wi[i] * si[i])

    return result_ot


def Am(vi, si):
    result_am = []

    for i in range(len(vi)):
        if (si[i] != None):
            result_am.append(vi[i] * si[i])

    return result_am
