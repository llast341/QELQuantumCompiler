import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import random_unitary
from qiskit_ibm_runtime.fake_provider import FakeAuckland, FakeWashington
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler import Target, InstructionProperties, CouplingMap
from qiskit.circuit.library import UGate, CXGate, UnitaryGate
from qiskit.circuit import Parameter
import networkx as nx

"""
This code creates a preset pass manager to transpile some quantum circuit, this is now the stock version of qiskit 
(more or less), so we aim to build something faster than this, that means decreasing the circuit depth
"""


# set the basis gate set
def get_basis_gates():
    return ['rx', 'rz', 'cp']


# create a linear chain of coupled qubits
def get_linear_coupling_map(number_of_qubits):
    coupling_map = []
    for i in range(number_of_qubits):
        coupling_map.append([i, i + 1])
        coupling_map.append([i + 1, i])
    return CouplingMap(coupling_map)


# create a rectangular map of qubits, where all nearest neighbors are connected symmetricly
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
        coupling_map.append([x * (y-1), x * (y-1) + 1])
        coupling_map.append([x * (y-1) + 1, x * (y-1)])
    return CouplingMap(coupling_map)


# get your coupling map
cmap = get_rectangle_map(7,3)
image = cmap.draw()
plt.imshow(image)
plt.axis('off')


# write your quantum circuit/algorithm, this shouldn't have more qubits than your coupling map obviously
UU = random_unitary(4, seed=12345)
rand_U = UnitaryGate(UU)

qc = QuantumCircuit(6)
qc.h(0)
qc.cx(0, range(1, 6))
qc.append(rand_U, range(2))
qc.swap(0, 1)
qc.draw('mpl')

# create a preset pass manager with our coupling map and our basis gates
pass_manager = generate_preset_pass_manager(
    optimization_level=3,
    coupling_map=cmap,
    layout_method="trivial",  # Fixed layout mapped in circuit order
    basis_gates=get_basis_gates(),
)
# print the transpiled circuit
pass_manager.run(qc).draw('mpl')

# get the circuit depht, to compare it to another way of transpiling
depths = []
for _ in range(100):
    depths.append(pass_manager.run(qc).depth())

plt.figure(figsize=(8, 6))
plt.hist(depths, align="left", color="#AC557C")
plt.xlabel("Depth", fontsize=14)
plt.ylabel("Counts", fontsize=14)
plt.show()