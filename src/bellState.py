from qiskit import QuantumCircuit, Aer, assemble, execute, BasicAer, QuantumRegister, ClassicalRegister
from math import pi, sqrt
import numpy as np
import math
from qiskit.visualization import plot_histogram, plot_bloch_multivector

# Construction of the circuit
qr = QuantumRegister(2)
qc = QuantumCircuit(qr)
qc.h(0)
qc.cx(0,1)

# Visualization of the circuit, statevector and bloch sphere representation
# Bloch Sphere representation will show no information as a result of entanglement
svsim = Aer.get_backend('statevector_simulator')
qobj = assemble(qc)
entangled_state = svsim.run(qobj).result()
stateVector = entangled_state.get_statevector()

print(qc)
print("\n\n", stateVector)
print("\n\n")
plot_bloch_multivector(stateVector)

# Visualization of probabilities
plot_histogram(entangled_state.get_counts())

# Construction of the measurement circuit
cr  = ClassicalRegister(2)
qMeasurement = QuantumCircuit(qr, cr)
for j in range(2):
   qMeasurement.measure(j,j)

# Construction and visualization of the final circuit
qcFinal = qc + qMeasurement
print(qcFinal, "\n")

# Execution of the circuit
backend = BasicAer.get_backend('qasm_simulator')
job = execute(qcFinal, backend, shots=1024)
results = job.result()
counts = results.get_counts(qcFinal)
print(counts)