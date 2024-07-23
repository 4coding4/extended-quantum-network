from netsquid.components import INSTR_Z, INSTR_X
from netsquid.protocols import NodeProtocol


# TODO check if this file is even used
class DirectCorrection(NodeProtocol):
    def run(self, m):
        meas_results = m
        if meas_results[0] == 1:
            self.node.qmemory.execute_instruction(INSTR_Z)
            yield self.await_program(self.node.qmemory)
        if meas_results[1] == 1:
            self.node.qmemory.execute_instruction(INSTR_X)
        yield self.await_program(self.node.qmemory)
