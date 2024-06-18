from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.circuit.library import HGate
import matplotlib.pyplot as plt
import numpy as np
import Equivalence_library as el


N = 15
def get_rectangle_map(x,y):
    coupling_map = []
    for j in range(y-1):
        for i in range(x-1):
            coupling_map.append([i+j*x, i+j*x+1])
            coupling_map.append([i+j*x+1, i+j*x])
            coupling_map.append([i+j*x, i+(j+1)*x])
            coupling_map.append([i+(j+1)*x, i+j*x])
    for i in range(1, y):
        coupling_map.append([x * i - 1, x * i + 1])
        coupling_map.append([x * i + 1, x * i - 1])
    for j in range(1,x):
        coupling_map.append([j * y + 1, j * y + 1])
        coupling_map.append([j * y + 1, j * y - 1])
    return coupling_map


cmap = get_rectangle_map(2,3)

print(cmap)