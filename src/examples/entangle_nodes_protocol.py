import netsquid.qubits.ketstates as ketstates

from pydynaa import EventExpression
from netsquid.nodes import Network, node
from netsquid.qubits import StateSampler
from netsquid import sim_run, qubits, b00
from netsquid.protocols.protocol import Signals
from netsquid.protocols.nodeprotocols import NodeProtocol
from netsquid.components import QuantumProcessor, QSource, SourceStatus, FixedDelayModel, QuantumChannel, INSTR_SWAP, \
    Port


PROCESS_POSITIONS: int = 3
SOURCE_MODEL_DELAY: int = 5
QUANTUM_CHANNEL_DELAY: int = 100


class EntangleNodes(NodeProtocol):
    """
    Cooperate with another node to generate shared entanglement.
    """
    _num_pairs: int = 0
    _is_source: bool = False
    _qsource_name: node = None
    _mem_positions: list = None
    _input_mem_position: int = 0
    _qmem_input_port: Port = None

    entangled_pairs_n: int = 0
    start_expression: EventExpression = None


    def __init__(self, on_node: node, is_source: bool, name: str, start_expression: EventExpression=None,
                 input_mem_pos: int=0, num_pairs: int=1) -> None:
        """
        Constructor for the EntangleNode protocol class.

        :param on_node: Node to run this protocol on
        :param is_source: Whether this protocol should act as a source or a receiver. Both are needed
        :param name: Name of the protocol
        :param start_expression: Event Expression to wait for before starting entanglement round
        :param input_mem_pos: Index of quantum memory position to expect incoming qubits on. Default is 0
        :param num_pairs: Number of entanglement pairs to create per round. If more than one, the extra qubits will be
                          stored on available memory positions
        """
        super().__init__(node=on_node, name=name)

        if start_expression is not None and not isinstance(start_expression, EventExpression):
            raise TypeError(f"Start expression should be a {EventExpression}, not a {type(start_expression)}")

        if self.node.qmemory is None:
            raise ValueError(f"Node {self.node} does not have a quantum memory assigned.")

        self._is_source = is_source
        self._num_pairs = num_pairs
        self._input_mem_position = input_mem_pos
        self._qmem_input_port = self.node.qmemory.ports[f"qin{self._input_mem_position}"]

        self.start_expression = start_expression
        self.node.qmemory.mem_positions[self._input_mem_position].in_use = True

    def start(self) -> NodeProtocol:
        """
        Start up the protocol by first claiming extra memory positions (if needed).

        :return: The Node Protocol
        """
        self._mem_positions = [self._input_mem_position]

        # Claim extra memory positions if needed
        extra_memory: int = self._num_pairs - 1

        if extra_memory > 0:
            unused_positions = self.node.qmemory.unused_positions

            if extra_memory > len(unused_positions):
                raise RuntimeError(f"Not enough unused memory: need {extra_memory}, have {len(unused_positions)}")
            for i in unused_positions[:extra_memory]:
                self._mem_positions.append(i)
                self.node.qmemory.mem_positions[i].in_use = True

        return super().start()

    def stop(self) -> None:
        """
        Stop the Node Protocol and unclaim all the claimed memory.
        """
        # Unclaim all memory positions
        if self._mem_positions:
            for i in self._mem_positions[1:]:
                self.node.qmemory.mem_positions[i].in_use = False

            self._mem_positions.clear()

        super().stop()

    def run(self) -> None:
        """
        Send entangled qubits of the source and destination nodes.
        """

        while True:
            # If no start expression specified, then limit generation to one round
            if self.start_expression is not None:
                yield self.start_expression
            elif self._is_source and self.entangled_pairs_n >= self._num_pairs:
                break

            # Iterate in reverse so that input_mem_pos is handled last
            for mem_pos in self._mem_positions[::-1]:
                if self._is_source:
                    self.node.subcomponents[self._qsource_name].trigger()

                yield self.await_port_input(self._qmem_input_port)

                if mem_pos != self._input_mem_position:
                    self.node.qmemory.execute_instruction(INSTR_SWAP, [self._input_mem_position, mem_pos])

                    if self.node.qmemory.busy:
                        yield self.await_program(self.node.qmemory)

                self.entangled_pairs_n += 1
                self.send_signal(Signals.SUCCESS, mem_pos)

    @property
    def is_connected(self) -> bool:
        if not super().is_connected:
            return False

        if self.node.qmemory is None:
            return False

        if self._mem_positions is None and len(self.node.qmemory.unused_positions) < self._num_pairs - 1:
            return False

        if self._mem_positions is not None and len(self._mem_positions) != self._num_pairs:
            return False

        if self._is_source:
            for name, subcomp in self.node.subcomponents.items():
                if isinstance(subcomp, QSource):
                    self._qsource_name = name
                    break
            else:
                return False

        return True


def network_setup() -> Network:
    """
    This function creates and returns a quantum network.


    Nodes
    -----
    Alice:
        - Quantum Processor
            - qin0: Connected to Quantum Source
        - Quantum Source
            - qout0: Forwards output to Quantum Channel
            - qout1: Connected to Quantum Memory

    Bob:
        - Quantum Processor
            - qin0: input from Quantum Channel is forwarded to Quantum Memory


    Channels
    --------
    QuantumChannel:
        - From: Alice
        - To: Bob


    Diagram
    -------
    +---------------------+                                      +---------------------+
    |                     | +----------------------------------+ |                     |
    | "NodeAlice:"        | |                                  | | "NodeBob:"          |
    | "QSource"           O-* "Connection: QuantumChannel -->" *-O "QuantumProcessor"  |
    | "QuantumProcessor"  | |                                  | |                     |
    |                     | +----------------------------------+ |                     |
    +---------------------+                                      +---------------------+


    :return: The assembled quantum network
    """

    # Create a quantum network and add the nodes Alice and Bob
    network: Network = Network("Entangle_nodes")
    alice: node = network.add_node("Alice")
    bob: node = network.add_node("Bob")

    # Add a Quantum Processor to each node in the network. The Quantum Processor is a quantum memory which is able to
    # execute quantum programs or instructions. The parameter `num_positions` indicates the number of available memory
    # positions should the processor have.
    alice.add_subcomponent(
        QuantumProcessor("QuantumMemoryAlice", num_positions=PROCESS_POSITIONS, fallback_to_nonphysical=True)
    )
    bob.add_subcomponent(
        QuantumProcessor("QuantumMemoryBob", num_positions=PROCESS_POSITIONS, fallback_to_nonphysical=True)
    )

    # Add a component that generates Qubits. The qubits generated by the component share a specified quantum state. The
    # generated qubits have state b00, this means `|00> + |11>`. Moreover, the source will distribute the generated qubits
    # over 2 ports, and the quantum source will generate pulses when its input ports are triggered. Finally, the `Fixed
    # Delay Model` is the model used to compute the time it takes to generate the pulse. Only one pulse can be handled
    # at a time.
    alice.add_subcomponent(
        QSource("QuantumSourceAlice", state_sampler=StateSampler([ketstates.b00]), num_ports=2,
                status=SourceStatus.EXTERNAL, models={"emission_delay_model": FixedDelayModel(delay=5)})
    )

    # Create a quantum channel and add the connection to the network. The connection is made between nodes Alice and
    # Bob. The quantum channel is placed from Alice to Bob.
    quantum_channel: QuantumChannel = QuantumChannel("QuantumChannel", delay=100)
    port_alice, port_bob = network.add_connection(alice, bob, channel_to=quantum_channel, label="quantum")

    # Set up ports in Alice's nodes. The method `forward_output` when called on a port forwards the value of that port
    # to another port – namely the port of the quantum connection. The second port of the quantum source component is
    # connected to the input of the quantum memory of the node.
    alice.subcomponents["QuantumSourceAlice"].ports["qout0"].forward_output(alice.ports[port_alice])
    alice.subcomponents["QuantumSourceAlice"].ports["qout1"].connect(alice.qmemory.ports["qin0"])

    # Set up the port in Bob's node. The quantum channel's port forwards the input to the input port of the quantum
    # memory of the node.
    bob.ports[port_bob].forward_input(bob.qmemory.ports["qin0"])

    return network


if __name__ == '__main__':
    qnetwork: Network = network_setup()

    protocol_alice = EntangleNodes(on_node=qnetwork.subcomponents["Alice"], is_source=True, name="ProtocolAlice")
    protocol_bob = EntangleNodes(on_node=qnetwork.subcomponents["Bob"], is_source=False, name="ProtocolBob")

    protocol_alice.start()
    protocol_bob.start()

    sim_run()

    q1, = qnetwork.subcomponents["Alice"].qmemory.peek(0)
    q2, = qnetwork.subcomponents["Bob"].qmemory.peek(0)

    # Compute the fidelity between the qubits quantum state and the reference state (`|00> + |11>`)
    print(f"Fidelity of generated entanglement: {qubits.fidelity([q1, q2], b00)}")
