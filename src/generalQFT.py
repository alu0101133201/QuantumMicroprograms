import numpy as np
from numpy import pi
from qiskit import QuantumCircuit, transpile, assemble, Aer, IBMQ, BasicAer, execute
from qiskit.visualization import plot_bloch_multivector

# Recursive function which implements all the rotations (h and qc gates)
def rotations(qc, n):
    if n == 0:
        return;
    n -= 1
    qc.h(n)
    for qubit in range(n):
        qc.cp(pi/2**(n-qubit), qubit, n)
    rotations(qc, n)
    return qc

# Function which add the swap gates 
def swapRegs(qc, n):
    for qubit in range(n//2):
        qc.swap(qubit, n - qubit - 1)
    return qc

# General function which builds the QFT circuit
def buildQFT(qc, n):
    rotations(qc, n)
    swapRegs(qc, n)
    return qc

# Build a QTF circuit with 4 qubits
qc = QuantumCircuit(4)
buildQFT(qc, 4)
qc.draw()

# Example with input 13 (1101)
inputqc = QuantumCircuit(4)
inputqc.x(0)
inputqc.x(2)
inputqc.x(3)
finalqc = inputqc + qc
finalqc.draw()

svsim = Aer.get_backend('statevector_simulator')
qobj = assemble(finalqc)
entangled_state = svsim.run(qobj).result()
stateVector = entangled_state.get_statevector()
plot_bloch_multivector(stateVector)