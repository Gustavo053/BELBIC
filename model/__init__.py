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
# SENSOR DE TENSÃO NA REALIMENTAÇÃO
kr = 1
taur = 0.06

tMax = 60
T = 0
h = 0.01
nPontos = round(tMax / h)

uMax = 3.3

eant = 0
iant = 0

vref1 = 1*numpy.ones(round(nPontos/2))
vref2 = 2*numpy.ones(round(nPontos/2))
vref = numpy.append(vref1, vref2)
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
    global eant
    global iant

    A = 0
    O = 0
    E = 0
    E_dot = 0

    rew = 0

    vi = 0.81
    wi = 1.0

    for i in range(1, nPontos):
        ve[i] = vref[i - 1] - vs[i - 1]
        # O BELBIC entra aqui
        ePlot[i] = ve[i]
        si, dedt, eantNew, iantNew = belbic.SI(ve[i], tMax, eant, iant)
        eant = eantNew
        iant = iantNew

        # rew/EC = abs(error)
        rew = abs(ve[i])

        viNew, wiNew = belbic.sensory_cortex(si, rew, A, E_dot, vi, wi)
        vi = viNew
        wi = wiNew

        O, E_dot = belbic.orbifrontal_cortex(wi, si, A, O, rew)
        A, E = belbic.amygdala(vi, si, A, O, rew)

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

    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.axis([-1, tMax, 0, 4])
    plt.plot(tPlot, vs, 'k', label='sensor output')
    plt.plot(tPlot, vref, 'b', label='reference')
    plt.legend()
    plt.title('Sensor output')
    plt.ylabel('terminal voltage (vt)')
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.axis([-1, tMax, 0, 3.5])
    plt.plot(tPlot, uPlot, 'k', label='control signal')
    plt.legend()
    plt.title('Control signal')
    plt.xlabel('time (s)')
    plt.ylabel('Voltage (V)')
    plt.grid()

    plt.show()

    # plt.plot(T, vs)
    # plt.ylabel('tempo')
    # plt.xlabel('sinal de controle')
    # plt.show()
