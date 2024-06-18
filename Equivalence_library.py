from qiskit import QuantumRegister
from qiskit.circuit import QuantumCircuit, Parameter
from qiskit.circuit.library import CXGate, HGate, RYGate, RXGate, SwapGate
from qiskit.circuit.equivalence_library import EquivalenceLibrary
import numpy as np


# Translate every gate into the basic GateSet of CPHASE; X(PI/2); Z(PHI)

def hadamard_decompose(qc, qubit):
    qc.rz(np.pi, qubit)
    qc.rx(np.pi/2, qubit)
    qc.rz(np.pi, qubit)


def cnot_decompose(qc, control, target):
    hadamard_decompose(qc, target)
    qc.cp(np.pi, control, target)  # CPHASE with phase pi between control and target
    hadamard_decompose(qc, target)


def swap_decompose(qc, qubit1, qubit2):
    cnot_decompose(qc, 0, 1)  # CNOT from qubit 0 to qubit 1
    cnot_decompose(qc, 1, 0)  # CNOT from qubit 1 to qubit 0
    cnot_decompose(qc, 0, 1)  # CNOT from qubit 0 to qubit 1


def get_equivalence_library():

    elibrary = EquivalenceLibrary()

    # Equivalent for Hadamard Gate
    h_equiv = QuantumCircuit(1)
    hadamard_decompose(h_equiv, 0)
    elibrary.add_equivalence(HGate(), h_equiv)

    # Equivalent for CNOT gate
    cnot_equiv = QuantumCircuit(2)
    cnot_decompose(cnot_equiv, 0, 1)
    elibrary.add_equivalence(CXGate(), cnot_equiv)

    # Equivalent for SWAP Gate
    swap_equiv = QuantumCircuit(2)
    swap_decompose(swap_equiv, 0, 1)
    elibrary.add_equivalence(SwapGate(), swap_equiv)

    return elibrary




