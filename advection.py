import matplotlib.pyplot as plt
import numpy as np


# Constants
NumberOfNodes = 100
l = 1.0     # speed (lambda in the equation)
k = 0.4
h = 2 / NumberOfNodes   # step
tau = abs(k * h / l)         # time step
NumberOfTimeSteps = int(2 / (h * k))
# NumberOfTimeSteps = 165
StencilByInterpolationOrder = {1: [-1, 0], 2: [-1, 0, 1], 3: [-2, -1, 0, 1], \
    4: [-2, -1, 0, 1, 2]}


def initialize(StartingConfiguration):
    NextTimeLayer = np.zeros(NumberOfNodes)
    if StartingConfiguration == 'rect':
        # rectangular impulse
        CurrentTimeLayer = np.zeros(NumberOfNodes)
        start, finish = int(np.floor(0.25 * NumberOfNodes)), int(np.floor(0.75 * NumberOfNodes))
        CurrentTimeLayer[start:finish] = 1.0
        return CurrentTimeLayer, NextTimeLayer
    elif StartingConfiguration == 'smooth':
        # [sin(pi*x)]^4 on [-1; 1]
        CurrentTimeLayer = np.empty(NumberOfNodes)
        for i in range(NumberOfNodes):
            x = -1 + i * h
            CurrentTimeLayer[i] = np.sin(np.pi * x) ** 4
        return CurrentTimeLayer, NextTimeLayer
    else:
        ErrorMessage = 'Invalid StartingConfiguration parameter'
        print(ErrorMessage)
        print(StartingConfiguration)
        exit(1)


def InterpolateValue(u):
    """ u is an array of values needed for interpolation
    """
    if l > 0:
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
        elif InterpolationOrder == 4:
            # y = a * x^4 + b * x^3 + c * x^2 + d * x + e
            a = (6 * u[2] - 4 * u[3] - 4 * u[1] + u[4] +u[0]) / (24 * h ** 4)
            b = (2 * u[1] - 2 * u[3] + u[4] - u[0]) / (12 * h ** 3)
            c = (16 * u[3] - 30 * u[2] + 16 * u[1] - u[4] - u[0]) / (24 * h ** 2)
            d = (8 * u[3] - 8 * u[1] - u[4] + u[0]) / (12 * h)
            e = u[2]
            x = -l * tau
            return a * x ** 4 + b * x ** 3 + c * x ** 2 + d * x + e
        else:
            ErrorMessage = 'InterpolationOrder should be an integer from {1, 2, 3, 4}'
            print(ErrorMessage)
            exit(1)
    # TODO!!! Negative lambda
    elif l < 0:
        pass


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


def DebugPlot(info):
    plt.plot(np.linspace(-1, 1, NumberOfNodes), CurrentTimeLayer)
    plt.xlabel('Coordinate')
    plt.ylabel('Value')
    plt.title('Advection - '+info)
    plt.grid(True)
    plt.show()


# main part
InterpolationOrder = int(input('InterpolationOrder = '))
StartingConfiguration = input("Input type of init ('rect' or 'smooth'): ")
stencil = StencilByInterpolationOrder[InterpolationOrder]
StencilValues = np.zeros(InterpolationOrder + 1)

CurrentTimeLayer, NextTimeLayer = initialize(StartingConfiguration)
DebugPlot('initial configuration')
for step in range(NumberOfTimeSteps):
    SingleStep()
    
    if step % 50 == 0 or step == 10 or step == 20 or step == 30 or step == 40:
        DebugPlot('step = '+str(step))
    """
    if step % 50 == 0:
        DebugPlot('step = '+str(step))
"""
print('Finished')
DebugPlot('Finished')
