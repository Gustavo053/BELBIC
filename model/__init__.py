import numpy
import belbic

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
t = 0
h = 0.01
nPontos = tMax/h

uMax = 20

vr = numpy.zeros(1, nPontos)
vf = numpy.zeros(1, nPontos)
vt = numpy.zeros(1, nPontos)
vs = numpy.zeros(1, nPontos)
uPlot = numpy.zeros(1, nPontos)
ePlot = numpy.zeros(1, nPontos)
vref = numpy.ones(1, nPontos)
ve = numpy.zeros(1, nPontos)


def amplifier(i, u):
    global vr
    vr[i] = vr[i-1] + (T/tau_a)*(-vr[i-1] + ka*u)

    return vr[i]


def exciter(i, vr):
    global vf
    vf[i] = vf[i-1] + (T/tau_e)*(-vf[i-1] + ke*vr)

    return vf[i]


def generator(i, vf):
    global vt
    vt[i] = vt[i-1] + (T/tau_g)*(-vt[i-1] + kg*vf)

    return vt[i]


def sensor(i, vt):
    global vs
    vs[i] = vs[i-1] + (T/tau_r)*(-vs[i-1] + kr*vt)

    return vs[i]


def run():
    global ve
    global vs
    for i in range(len(nPontos)):
        ve[i] = vref[i - 1] - vs[i - 1]
        # O BELBIC vai entrar aqui
        ePlot[i] = ve[i]
        si, dedt = belbic.SI(ve[i], tMax)
        vi, wi = belbic.sensory_cortex(si)
        O, E_dot = belbic.orbifrontal_cortex(wi, si, ve[i])  # ve[i] = rew/EC
        A, E = belbic.amygdala(vi, si, ve[i])  # ve[i] = rew/EC

        uPlot[i] = A - O  # (signal amydgala) - (signal orbitofrontal cortex)

        if (uPlot[i] >= uMax):
            uPlot[i] = uMax
        elif (uPlot[i] <= 0):
            uPlot[i] = 0

        vr = amplifier(i, uPlot[i])
        vf = exciter(i, vr)
        vt = generator(i, vf)
        vs = sensor(i, vt)
