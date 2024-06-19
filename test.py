from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.circuit.library import HGate
import matplotlib.pyplot as plt
import numpy as np
from qiskit.transpiler import CouplingMap

import Equivalence_library as el


cmap = CouplingMap([[0, 1], [1, 2], [2, 0], [3, 4], [4, 5], [5, 3]])
component_cmaps = cmap.connected_components()
image = cmap.draw()

plt.imshow(image)
plt.axis('off')
plt.show()