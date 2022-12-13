from netsquid.components import QSource, Port, INSTR_SWAP
from netsquid.nodes import node
from netsquid.protocols import NodeProtocol
from netsquid.protocols.protocol import Signals


class GenerateEntanglement(NodeProtocol):
    """
    Generate shared entanglement between two nodes.
    """
    _is_source: bool = False
    _is_repeater: bool = False
    _is_remote: bool = False
    _qsource_name: node = None
    _qmem_input_ports: [Port] = []


    def __init__(self, on_node: node, name: str, is_source: bool = False, is_repeater: bool = False,
                 is_remote: bool = False):
        """
        Constructor for the GenerateEntanglement protocol class.

        :param on_node: Node to run this protocol on
        :param is_source: Whether this protocol should act as a source or a receiver. Both are needed
        :param is_repeater: Whether this protocol should act as a repeater
        :param is_remote: Whether this protocol should act as a remote_source
        :param name: Name of the protocol
        """
        super().__init__(node=on_node, name=name)

        self._is_source = is_source
        self._is_repeater = is_repeater
        self._is_remote = is_remote

        if not self._is_source:
            self._qmem_input_ports.append(self.node.qmemory.ports["qin0"])
            self.node.qmemory.mem_positions[0].in_use = True

        if self._is_repeater:
            self._qmem_input_ports.append(self.node.qmemory.ports["qin1"])
            self.node.qmemory.mem_positions[1].in_use = True


    def run(self) -> None:
        """
        Send entangled qubits of the source to the two destination nodes.
        """
        if self._is_source or self._is_remote:
            self.node.subcomponents[self._qsource_name].trigger()

        if not self._is_source:
            yield self.await_port_input(self._qmem_input_ports[0])
            self.send_signal(Signals.SUCCESS, 0)

        if self._is_remote:
            yield self.await_port_input(self._qmem_input_ports[1])
            self.send_signal(Signals.SUCCESS, 1)


    @property
    def is_connected(self) -> bool:
        if self._is_source or self._is_remote:
            for name, subcomp in self.node.subcomponents.items():
                if isinstance(subcomp, QSource):
                    self._qsource_name = name
                    break
            else:
                return False

        return True
