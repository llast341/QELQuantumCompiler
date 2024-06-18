import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeAuckland, FakeWashington
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler import Target, InstructionProperties, CouplingMap
from qiskit.circuit.library import UGate, CXGate
from qiskit.circuit import Parameter


def get_basis_gates():
    return ['rx', 'rz', 'cp']


def get_linear_coupling_map(number_of_qubits):
    coupling_map = []
    for i in range(number_of_qubits):
        coupling_map.append([i, i + 1])
        coupling_map.append([i + 1, i])
    return coupling_map


def get_rectangle_map(x,y):
    coupling_map = []
    for i in range(x):
        for j in range(y):
            coupling_map.append([i+j*x, i+j*x+1])
            coupling_map.append([i+j*x+1, i+j*x])
            coupling_map.append([i+j*x, i+(j+1)*x])
            coupling_map.append([i+(j+1)*x, i+j*x])


cmap = get_linear_coupling_map(15)

ghz = QuantumCircuit(15)
ghz.h(0)
ghz.cx(0, range(1, 15))
ghz.draw('mpl')

pass_manager = generate_preset_pass_manager(
    optimization_level=3,
    coupling_map=cmap,
    layout_method="trivial",  # Fixed layout mapped in circuit order
    basis_gates=get_basis_gates(),
)
pass_manager.run(ghz).draw('mpl')

depths = []
for _ in range(100):
    depths.append(pass_manager.run(ghz).depth())

plt.figure(figsize=(8, 6))
plt.hist(depths, align="left", color="#AC557C")
plt.xlabel("Depth", fontsize=14)
plt.ylabel("Counts", fontsize=14)
plt.show()