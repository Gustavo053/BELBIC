import numpy
import belbic
import matplotlib.pyplot as plt


# AMPLIFICADOR
ka = 10  # 10 a 400
taua = 0.1
# EXCITADOR
ke = 1
taue = 1
# GERADOR
kg = 1
taug = 1
# SENSOR DE TENS�O NA REALIMENTA��O
kr = 1
taur = 0.06

tMax = 20
T = 0
h = 0.01
nPontos = round(tMax / h)

uMax = 5

eantTest = 0
iantTest = 0

vref = 1*numpy.ones(nPontos)
vr = numpy.zeros(nPontos)
vf = numpy.zeros(nPontos)
vt = numpy.zeros(nPontos)
vs = numpy.zeros(nPontos)
ve = numpy.zeros(nPontos)
uPlot = numpy.zeros(nPontos)
ePlot = numpy.zeros(nPontos)

tPlot = numpy.linspace(0, tMax, nPontos)


def amplifier(i, vr, u):
    global h
    global taua
    global ka

    # print(ka*u)

    vr[i] = vr[i-1] + (h/taua)*(-vr[i-1] + ka*u)

    # print(vr[i])

    return vr


def exciter(i, vf, vr):
    global h
    global taue
    global ke

    vf[i] = vf[i-1] + (h/taue)*(-vf[i-1] + ke*vr)

    return vf


def generator(i, vt, vf):
    global h
    global taug
    global kg

    vt[i] = vt[i-1] + (h/taug)*(-vt[i-1] + kg*vf)

    return vt


def sensor(i, vs, vt):
    global h
    global taur
    global kr

    vs[i] = vs[i-1] + (h/taur)*(-vs[i-1] + kr*vt)

    return vs


def run():
    global ve
    global vs
    global vf
    global vr
    global vt
    global vref
    global T
    global eantTest
    global iantTest

    # eant = 0
    # iant = 0

    A = 0
    O = 0
    E = 0
    E_dot = 0
    for i in range(1, nPontos):
        # print(eant)
        ve[i] = vref[i - 1] - vs[i - 1]
        # print(f'error: ', ve[i])
        # O BELBIC vai entrar aqui
        ePlot[i] = ve[i]
        si, dedt, eant, iant = belbic.SI(ve[i], tMax, eantTest, iantTest)
        eantTest = eant
        iantTest = iant
        vi, wi = belbic.sensory_cortex(si, ve[i]**2, A, E_dot)

        # ve[i] = rew/EC
        O, E_dot = belbic.orbifrontal_cortex(wi, si, A, O, ve[i]**2)
        A, E = belbic.amygdala(vi, si, A, O, ve[i]**2)  # ve[i] = rew/EC

        uPlot[i] = A - O  # (signal amydgala) - (signal orbitofrontal cortex)

        if (uPlot[i] >= uMax):
            uPlot[i] = uMax
        elif (uPlot[i] <= 0):
            uPlot[i] = 0

        vr = amplifier(i, vr, uPlot[i])
        vf = exciter(i, vf, vr[i])
        vt = generator(i, vt, vf[i])
        vs = sensor(i, vs, vt[i])

        # print('---------PLANTA---------')

        # print(f'vr: ', vr[i])
        # print(f'vf: ', vf[i])
        # print(f'vt: ', vt[i])
        # print(f'vs: ', vs[i])

    plt.plot(tPlot, vs, 'k', label='sensor output')
    plt.legend()
    plt.title('Saída do sensor')
    plt.xlabel('time (s)')
    plt.ylabel('terminal voltage (vt)')
    plt.show()

    # plt.plot(T, vs)
    # plt.ylabel('tempo')
    # plt.xlabel('sinal de controle')
    # plt.show()
