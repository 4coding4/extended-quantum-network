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
                 is_remote: bool = False, qsource_name: node = None):
        """
        Constructor for the GenerateEntanglement protocol class.

        :param on_node: Node to run this protocol on
        :param name: Name of the protocol
        :param is_source: Whether this protocol should act as a source or a receiver. Both are needed
        :param is_repeater: Whether this protocol should act as a repeater
        :param is_remote: Whether this protocol should act as a remote_source
        :param qsource_name: Name of the qsource node to use for this protocol. If None, the first source node is used.
        """
        super().__init__(node=on_node, name=name)

        self._is_source = is_source
        self._is_repeater = is_repeater
        self._is_remote = is_remote
        self._qsource_name = qsource_name  # default is None

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
            # handle first when the _qsource_name is set/passed as parameter, check if the source is connected
            if self._qsource_name is not None:
                for name, subcomp in self.node.subcomponents.items():
                    if isinstance(subcomp, QSource):
                        if self._qsource_name is name:
                            # no need to set _qsource_name again, it is already set
                            return True
                return False
            # handle when the _qsource_name is not set, check if the first source is connected
            else:
                for name, subcomp in self.node.subcomponents.items():
                    if isinstance(subcomp, QSource):
                        # connect the first source found
                        self._qsource_name = name
                        return True
                return False  # no source connected/found
        # needed for repeater nodes
        else:
            return True
