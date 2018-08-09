import matplotlib.pyplot as plt
import numpy as np


# Constants
NumberOfNodes = 100
l = 1.0     # speed (lambda in the equation)
k = 0.4     # something
h = 2 / NumberOfNodes   # step
tau = k * h / l         # time step
NumberOfTimeSteps = int(2 / (h * k))
# NumberOfTimeSteps = 165
StencilByInterpolationOrder = {1: [-1, 0], 2: [-1, 0, 1], 3: [-2, -1, 0, 1]}


def initialize(StartingConfiguration):
    NextTimeLayer = np.zeros(NumberOfNodes)
    dNextTimeLayer = np.zeros(NumberOfNodes)
    if StartingConfiguration == 'rect':
        # rectangular impulse
        dCurrentTimeLayer = np.zeros(NumberOfNodes)
        CurrentTimeLayer = np.zeros(NumberOfNodes)
        start, finish = np.floor(0.25 * NumberOfNodes), np.floor(0.75 * NumberOfNodes)
        CurrentTimeLayer[start:finish] = 1.0
        return CurrentTimeLayer, NextTimeLayer, dCurrentTimeLayer, dNextTimeLayer
    elif StartingConfiguration == 'smooth':
        # [sin(pi*x)]^4 on [-1; 1]
        CurrentTimeLayer = np.empty(NumberOfNodes)
        dCurrentTimeLayer = np.empty(NumberOfNodes)
        for i in range(NumberOfNodes):
            x = -1 + i * h
            CurrentTimeLayer[i] = np.sin(np.pi * x) ** 4
            dCurrentTimeLayer[i] = 4 * np.pi * np.cos(np.pi * x) ** 3
        return CurrentTimeLayer, NextTimeLayer, dCurrentTimeLayer, dNextTimeLayer
    else:
        ErrorMessage = 'Invalid StartingConfiguration parameter'
        print(ErrorMessage)
        print(StartingConfiguration)
        exit(1)


def InterpolateValue(u, du):
    """ u is an array of values needed for interpolation
    """
    if InterpolationOrder == 3:
        # Qubic interpolation: y = a * x^3 + b * x^2 + c * x + d
        a = (du[1] + du[0]) / h**2 - 2 * (u[1] - u[0]) / h**3
        b = (2 * du[1] + du[0]) / h - 3 * (u[1] - u[0]) / h**2
        c = du[1]
        d = u[1]
        x = -l * tau
        return a * x ** 3 + b * x ** 2 + c * x + d
    elif InterpolationOrder == 5:
        # TODO!!! Now it doesn't work
        # Quadratic interpolation : y = a * x^2 + b * x + c
        pass
    else:
        ErrorMessage = 'InterpolationOrder should be 3'
        print(ErrorMessage)
        exit(1)


def InterpolateDValue(u, du):
    if InterpolationOrder == 3:
        """ Qubic interpolation: y = a * x^3 + b * x^2 + c * x + d,
        returning dy = 3 * a * x^2 + 2 * b * x + c
        """
        a = (du[1] + du[0]) / h**2 - 2 * (u[1] - u[0]) / h**3
        b = (2 * du[1] + du[0]) / h - 3 * (u[1] - u[0]) / h**2
        c = du[1]
        d = u[1]
        x = -l * tau
        return 3 * a * x**2 + 2 * b * x + c
    else:
        ErrorMessage = 'InterpolationOrder should be 3'
        print(ErrorMessage)
        exit(1)    


def FillStencilValues(index):
    for i in stencil:
        j = (index + i) % NumberOfNodes
        StencilValues[i] = CurrentTimeLayer[j]
        StencilDValues[i] = dCurrentTimeLayer[j]


def SingleStep():
    """ Single step of the algorithm
    """
    global NextTimeLayer, CurrentTimeLayer, dNextTimeLayer, dCurrentTimeLayer
    for i in range(NumberOfNodes):
        FillStencilValues(i)
        NextTimeLayer[i] = InterpolateValue(StencilValues, StencilDValues)
        dNextTimeLayer[i] = InterpolateDValue(StencilValues, StencilDValues)
    CurrentTimeLayer, NextTimeLayer = NextTimeLayer, CurrentTimeLayer  # should be working faster then copying
    dCurrentTimeLayer, dNextTimeLayer = dNextTimeLayer, dCurrentTimeLayer


def DebugPrint():
    eps = 0.1
    for i in range(NumberOfNodes):
        if abs(CurrentTimeLayer[i]) < eps:
            print('_', end='')
        else:
            print('|', end='')
    print('')


def DebugPlot(info):
    plt.plot(np.linspace(-1, 1, NumberOfNodes), CurrentTimeLayer)
    plt.xlabel('Coordinate')
    plt.ylabel('Value')
    plt.title('Advection - '+info)
    plt.show()


# main part
InterpolationOrder = int(input('InterpolationOrder = '))
StartingConfiguration = input("Input type of init ('rect' or 'smooth'): ")

s = (InterpolationOrder + 1) // 2
stencil = StencilByInterpolationOrder[s]
StencilValues = np.empty(s)
StencilDValues = np.empty(s)

CurrentTimeLayer, NextTimeLayer, dCurrentTimeLayer, \
    dNextTimeLayer = initialize(StartingConfiguration)

DebugPrint()
for step in range(NumberOfTimeSteps):
    SingleStep()
    if step % 50 == 0:
        DebugPlot('step = '+str(step))

print('Finished')
DebugPrint()
DebugPlot('Finished')