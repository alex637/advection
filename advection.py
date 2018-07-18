# FIXME: redo using numpy

import math


# Constants
NumberOfNodes = 100
l = 1.0     # speed (lambda in the equation)
k = 0.4     # TODO!!! - what is this
h = 2 / NumberOfNodes   # step
tau = k * h / l         # time step
NumberOfTimeSteps = int(2 / (h * k))
StencilByInterpolationOrder = {1: [-1, 0], 2: [-1, 0, 1], 3: [-2, -1, 0, 1]}


def initialize(StartingConfiguration):
    if StartingConfiguration == 'rect':
        # rectangular impulse
        for i in range(NumberOfNodes):
            NextTimeLayer[i] = 0.0
            if NumberOfNodes * 0.25 <= i <= NumberOfNodes * 0.75:
                CurrentTimeLayer[i] = 1.0
            else:
                CurrentTimeLayer[i] = 0.0
    elif StartingConfiguration == 'smooth':
        # [sin(pi*x)]^4 on [-1; 1]
        for i in range(NumberOfNodes):
            NextTimeLayer[i] = 0.0
            x = -1 + i * h
            CurrentTimeLayer[i] = math.sin(math.pi * x) ** 4

    else:
        ErrorMessage = 'Invalid StartingConfiguration parameter'
        print(ErrorMessage)
        print(StartingConfiguration)
        exit(1)


def InterpolateValue(u):
    """ u is an array of values needed for interpolation
    """
    if InterpolationOrder == 1:
        # linear interpolation: y = a*x + b
        a = (u[1] - u[0]) / h
        b = u[1]
        x = -l * tau
        return a * x + b
    elif InterpolationOrder == 2:
        # Quadratic interpolation : y = a * x^2 + b * x + c
        a = (u[2] - 2 * u[1] + u[0]) / (2 * h**2)
        b = (u[2] - u[0]) / (2 * h)
        c = u[1]
        x = -l * tau
        return a * x ** 2 + b * x + c
    elif InterpolationOrder == 3:
        # Qubic interpolation: y = a * x^3 + b * x^2 + c * x + d
        a = (u[3] + 3 * u[1] - 3 * u[2] - u[0]) / (6 * h**3)
        b = (u[3] - 2 * u[2] + u[1]) / (2 * h**2)
        c = (2 * u[3] + 3 * u[2] - 6 * u[1] + u[0]) / (6 * h)
        d = u[2]
        x = -l * tau
        return a * x ** 3 + b * x ** 2 + c * x + d


def SingleStep():
    """ Single step of the algorithm
    """
    global NextTimeLayer, CurrentTimeLayer
    for i in range(NumberOfNodes):
        FillStencilValues(i)
        NextTimeLayer[i] = InterpolateValue(StencilValues)  # StencilValues is a global list
    CurrentTimeLayer, NextTimeLayer = NextTimeLayer, CurrentTimeLayer  # shold be working faster then copying


def FillStencilValues(index):
    for i in stencil:
        StencilValues[i] = CurrentTimeLayer[(index + i) % NumberOfNodes]


def DebugPrint():
    eps = 0.1
    for i in range(NumberOfNodes):
        if abs(CurrentTimeLayer[i]) < eps:
            print('_', end='')
        else:
            print('|', end='')
    print('')


def DebugPlot():
    # TODO!!!
    pass

# main part
InterpolationOrder = int(input('InterpolationOrder = '))
StartingConfiguration = input("Input type of init ('rect' or 'smooth'): ")
# CurrentTimeLayer = [None for i in range(NumberOfNodes)]
# NextTimeLayer = [None for i in range(NumberOfNodes)]
CurrentTimeLayer = [None] * NumberOfNodes
NextTimeLayer = [None] * NumberOfNodes
stencil = StencilByInterpolationOrder[InterpolationOrder]
# StencilValues = [None for i in range(InterpolationOrder)]
StencilValues = [None] * (InterpolationOrder + 1)

initialize(StartingConfiguration)
DebugPrint()
for step in range(NumberOfTimeSteps):
    SingleStep()
    if step % 10 == 0 and step > 0:
        print('step is', step)
        DebugPrint()
print('Finished')
DebugPrint()
