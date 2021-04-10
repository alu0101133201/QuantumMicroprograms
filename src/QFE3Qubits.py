import numpy as np
from numpy import pi
from qiskit import QuantumCircuit, transpile, assemble, Aer, IBMQ, BasicAer, execute
from qiskit.visualization import plot_histogram, plot_bloch_multivector

# Construction of the circuit that will encode the phase
phaseCodification = QuantumCircuit(4)
numberOfGates = 1

phaseCodification.x(3)
for qubit in range(3):
    phaseCodification.h(qubit)

for qubit in range(3):
    for gateIter in range(numberOfGates):
        phaseCodification.cp(pi/2, qubit, 3)
    numberOfGates *= 2

phaseCodification.draw()

# Construction of the circuit which implements the inverse QFT
inverseQFT = QuantumCircuit(4)

inverseQFT.swap(0, 2)
inverseQFT.h(0)
inverseQFT.cp(-pi/2, 0, 1)
inverseQFT.h(1)
inverseQFT.cp(-pi/4, 1, 2)
inverseQFT.cp(-pi/2, 1, 2)
inverseQFT.h(2)

inverseQFT.draw()

# Measurement circuit
measurement = QuantumCircuit(4,3)
for qubit in range(3):
    measurement.measure(qubit, qubit)
measurement.draw()

# Print phase + inverseQFT circuit
finalqc = phaseCodification + inverseQFT

svsim = Aer.get_backend('statevector_simulator')
qobj = assemble(finalqc)
entangled_state = svsim.run(qobj).result()
stateVector = entangled_state.get_statevector()

plot_bloch_multivector(stateVector)
plot_histogram(entangled_state.get_counts())

# Print phase + inverseQFT circuit + measurement
finalqc = phaseCodification + inverseQFT + measurement

svsim = Aer.get_backend('statevector_simulator')
qobj = assemble(finalqc)
entangled_state = svsim.run(qobj).result()
stateVector = entangled_state.get_statevector()

plot_bloch_multivector(stateVector)
plot_histogram(entangled_state.get_counts())