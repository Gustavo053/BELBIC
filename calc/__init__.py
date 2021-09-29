def Ath(sensors):
    bigger = max(sensors)
    return bigger


def delta_vi(alpha, sensors_input, rew, A):
    v = alpha * (sensors_input * max(0, rew - sensors_input))

    # print(f'vi: ', v)
    return v


def delta_wi(beta, sensors_input, rew, E_dot):
    w = beta * (sensors_input * (E_dot - rew))

    # print(f'wi: ', w)

    return w


def e(A, O):
    # sum_a = 0
    # sum_o = 0
    result_e = 0
    # for i in A:
    #     sum_a = sum_a + i

    # for j in O:
    #     sum_o = sum_o + j

    result_e = A - O

    return result_e


def e_dot(A, O):
    # sum_a = 0
    # sum_o = 0
    result_e_dot = 0
    # for i in A:
    #     sum_a = sum_a + i

    # for j in O:
    #     sum_o = sum_o + j

    result_e_dot = A - O

    return result_e_dot


def Ot(wi, si):
    result_ot = wi * si

    return result_ot


def Am(vi, si):
    result_am = vi * si

    return result_am
