from netsquid.components import INSTR_CNOT, INSTR_H, INSTR_MEASURE, INSTR_MEASURE_BELL, Message
from netsquid.components.qprocessor import QuantumProgram
from netsquid.nodes import DirectConnection
from netsquid.protocols import NodeProtocol
from netsquid.protocols.protocol import Signals
from src.protocols import DirectCorrection


class BellMeasurementProgram(QuantumProgram):
    default_num_qubits = 2

    def program(self):
        q1, q2 = self.get_qubit_indices(2)

        # self.apply(INSTR_CNOT, [q1, q2])
        # self.apply(INSTR_H, q1)
        # self.apply(INSTR_MEASURE, q1, output_key="M1")
        # self.apply(INSTR_MEASURE, q2, output_key="M2")
        self.apply(INSTR_MEASURE_BELL, [q1, q2], output_key="M")

        yield self.run()


class BellMeasurement(NodeProtocol):
    def run(self):
        qubit_initialised = False
        entanglement_ready = False
        measure_program = BellMeasurementProgram()

        while True:
            expr = yield self.await_program(self.node.qmemory)

            if expr.first_term.value:
                qubit_initialised = True
            else:
                entanglement_ready = True

            if qubit_initialised and entanglement_ready:
                yield self.node.qmemory.execute_program(measure_program)
                # m1, = measure_program.output["M1"]
                # m2, = measure_program.output["M2"]
                m, = measure_program.output("M")
                # self.node.ports["cout_repeater"].tx_output(Message(m))
                # self.send_signal(Signals.SUCCESS)
                # qubit_initialised = False
                # entanglement_ready = False
                DirectConnection(self._network.subcomponents["RemoteNode"], m=m).start()
