from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit.library import HGate
import matplotlib.pyplot as plt
import numpy as np

qc = QuantumCircuit(2,2)
qc.x(0)
qc.h(1)
qc.swap(0, 1)
qc.h(0)
print(qc.data)
qc.draw("mpl")
qc.data[1].operation.definition.draw('mpl')
qc.data[2].operation.definition.draw('mpl')

qc2 = QuantumCircuit(1)
qc2.append(
    HGate(),
    [0]
)
qc2.draw("mpl")

plt.show()