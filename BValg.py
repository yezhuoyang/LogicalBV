import qiskit
from typing import List, Union, Any
import numpy as np
from qiskit_aer import AerSimulator

def convert_int_to_list(num_qubits: int, alginput: int):
    controllist = []
    k = alginput
    for i in range(0, num_qubits):
        controllist.insert(0, k % 2)
        k = (k >> 1)
    return controllist


def convert_list_to_int(num_qubits: int, bitlist: List):
    result = 0
    for i in range(num_qubits):
        result = result + (bitlist[i] << (num_qubits - 1 - i))
    return result

class QuantumAlgorithm:

    def __init__(self, num_qubits: int) -> None:
        self.num_qubits = num_qubits

    def construct_circuit(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement construct_circuit method.")

    def clear_circuit(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement construct_circuit method.")


    def set_input(self, alginput: List) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement set_input method.")

    def compute_result(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement compute_result method.")


class BVAlgorithm_qiskit(QuantumAlgorithm):

    def __init__(self, num_qubits: int) -> None:
        super().__init__(num_qubits)
        self.num_qubits = num_qubits
        self.circuit = qiskit.QuantumCircuit(num_qubits, num_qubits - 1)
        self.simulator = AerSimulator()
        self.computed = False
        self._a = 0
        self._b = 0
        self.computed_a_value = -1

    '''
    The circuit structure is the same as DuetchJosa
    '''

    def construct_circuit(self) -> None:
        inputdim = self.num_qubits - 1
        '''
        The first layer of Hadmard 
        '''
        self.circuit.x(inputdim)
        self.circuit.h(list(range(0, self.num_qubits)))
        self.compile_func()
        self.circuit.h(list(range(0, self.num_qubits)))
        self.circuit.measure(list(range(0, self.num_qubits - 1)), list(range(0, self.num_qubits - 1)))

    '''
    The input of Berstain vazirani is a linear function f(x)=ax+b.
    We are asked to calculate a,b.
    b is 0 or 1
    a is a n-bit number. a<=((1<<numberqubit-1)-1)
    '''

    def set_input(self, parameter: List) -> None:
        if len(parameter) != 2:
            raise ValueError("Berstain vazirani must have two input parameter a,b!")
        self._a = parameter[0]
        self._b = parameter[1]
        if self._b != 0 and self._b != 1:
            raise ValueError("b has to be 0 or 1")
        if not (0 <= self._a < (1 << (self.num_qubits - 1))):
            raise ValueError("a out of range")

    def compile_func(self) -> None:
        alist = convert_int_to_list(self.num_qubits - 1, self._a)
        for i in range(0, self.num_qubits - 1):
            if alist[i] == 1:
                self.circuit.cx(i, self.num_qubits - 1)
        if self._b == 1:
            self.circuit.x(self.num_qubits - 1)
        return

    def compute_result(self) -> None:
        compiled_circuit = qiskit.transpile(self.circuit, self.simulator)

        # Execute the circuit on the aer simulator
        job = self.simulator.run(compiled_circuit, shots=1)

        # Grab results from the job
        result = job.result()
        # print(result)
        # Returns counts
        counts = result.get_counts(compiled_circuit)
        result = list(counts.keys())[0]
        self.computed = True
        self.computed_a_value = int(result[::-1], 2)
        print(f"The function is f(x)={result[::-1]}x+{self._b}")

    def a_result(self) -> int:
        return self.computed_a_value


    def set_simulator(self,simulator):
        self._simulator=simulator
        
        
'''
The logic version of Berstain vazirani algorithm using [4,2,2] code
'''
def logicBValgorithm(QuantumAlgorithm):
    def __init__(self, num_qubits: int) -> None:
        self.num_qubits = num_qubits

    def logicX(self,index):
        pass    
    
    def logicH(self,index):
        pass 
    
    def logicCNOT(self,control,target):
        pass 

    def logicCZ(self,control,target):
        pass
    
    
    def construct_circuit(self) -> None:
        inputdim = self.num_qubits - 1
        '''
        The first layer of Hadmard 
        '''
        self.logicX(inputdim)
        self.logicH(list(range(0, self.num_qubits)))
        self.compile_func()
        self.logicH(list(range(0, self.num_qubits)))
        self.circuit.measure(list(range(0, self.num_qubits - 1)), list(range(0, self.num_qubits - 1)))



    def clear_circuit(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement construct_circuit method.")


    def compile_func(self) -> None:
        alist = convert_int_to_list(self.num_qubits - 1, self._a)
        for i in range(0, self.num_qubits - 1):
            if alist[i] == 1:
                self.logicCNOT(i, self.num_qubits - 1)
                #self.circuit.cx(i, self.num_qubits - 1)
        if self._b == 1:
            #self.circuit.x(self.num_qubits - 1)
            self.logicX(self.num_qubits - 1)
        return

    def set_input(self, parameter: List) -> None:
        if len(parameter) != 2:
            raise ValueError("Berstain vazirani must have two input parameter a,b!")
        self._a = parameter[0]
        self._b = parameter[1]
        if self._b != 0 and self._b != 1:
            raise ValueError("b has to be 0 or 1")
        if not (0 <= self._a < (1 << (self.num_qubits - 1))):
            raise ValueError("a out of range")


    def compute_result(self) -> NotImplementedError:
        raise NotImplementedError("Subclasses must implement compute_result method.")    


        

if "__main__" == __name__:
    
    alg = BVAlgorithm_qiskit(20)
    # Initialize a random a and b, such that the input function is f(x)=ax+b
    a=0b1111111111111111111
    b=0
    alg.set_input([a,b])
    alg.construct_circuit()
    alg.compute_result()
