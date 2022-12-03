from netsquid import sim_run, qubits, b00
from netsquid.components import QuantumChannel, QSource, SourceStatus, FixedDelayModel, QuantumProcessor
from netsquid.nodes import Network, node
from netsquid.qubits import StateSampler, ketstates

from src.network.PortPair import PortPair
from src.protocols.GenerateEntanglement import GenerateEntanglement


class StarNetwork:
    """
    Class to create a star network topology. The center of the network is composed of a Node with only a Quantum Source
    as a component. All the other nodes are composed by quantum processors, and are connected to the source node by
    means of quantum connections.


    Default network topology
    ------------------------
                 +-----+
                 | N1  |
                 +-----+
                    ^
                    |
                   QC1
                    |
    +----+        +---+        +----+
    | N4 | <-QC4- | S | -QC2-> | N2 |
    +----+        +---+        +----+
                    |
                   QC3
                    |
                    v
                 +-----+
                 | N3  |
                 +-----+


    Nodes
    -----
    S:
        - Quantum Source

    Ni:
        - Quantum Processor
        - Quantum Memory (3x Memory positions)


    Channels
    --------
    QCi:
        - Unidirectional Quantum Channel (s -> Ni)


    Network properties
    ------------------
    destinations_n (default: 4):
        The number of destination nodes in the network

    source_delay (default: 5.0):
        Delay of the delay model of the quantum source in nanoseconds

    channels_length (default: 10):
        The length of the quantum channels in km
    """
    _destinations_n: int = 4
    _source_delay: float = 5.0
    _channels_length: int = 10

    # Network object and network components
    _network: Network = Network("StarNetwork")

    _source: node = None
    _destinations: [node] = []

    _quantum_channels: [QuantumChannel] = []
    _quantum_channels_port_pairs: [PortPair] = []


    def __init__(self):
        """
        Constructor for the StarNetwork class.
        """
        self._init_source()
        self._init_destinations()
        self._init_quantum_channels()

    ###########
    # GETTERS #
    ###########

    @property
    def network(self) -> Network:
        """
        :type: Network
        """
        return self._network

    @property
    def source_delay(self) -> float:
        """
        :type: float
        """
        return self._source_delay

    @property
    def destinations_n(self) -> int:
        """
        :type: int
        """
        return self._destinations_n

    ###########
    # SETTERS #
    ###########

    @source_delay.setter
    def source_delay(self, ns: float):
        """
        Set the source delay in nanoseconds (ns).

        :param ns: The amount of nanoseconds
        :raise: AssertionError If ns is 0.0 or less
        """
        assert (ns >= 0.0)
        self._source_delay = ns

    @destinations_n.setter
    def destinations_n(self, n: int):
        """
        Set the number of destination nodes in the network.

        :param n: The number of nodes
        :raise: AssertionError If n is 0 or less
        """
        assert (n > 0)
        self._destinations_n = n

    #############################################
    # PRIVATE HELPERS USED TO BUILD THE NETWORK #
    #############################################

    def _init_source(self):
        """
        Initialize the source node of the network.
        """
        self._source = self._network.add_node("Source")
        self._source.add_subcomponent(
            QSource("QuantumSource", state_sampler=StateSampler([ketstates.b00]), status=SourceStatus.EXTERNAL,
                    models={"emission_delay_model": FixedDelayModel(delay=self._source_delay)},
                    num_ports=2)
        )

    def _init_destinations(self):
        """
        Initialize the destination nodes of the network.
        """
        for destination_n in range(1, self._destinations_n + 1):
            self._destinations.append(self._network.add_node(f"Node{destination_n}"))
            self._destinations[destination_n - 1].add_subcomponent(
                QuantumProcessor(f"QP_Node{destination_n}", num_positions=3, fallback_to_nonphysical=True)
            )

    def _init_quantum_channels(self):
        """
        Initialize the quantum channels of the network.
        """
        for (index, destination) in enumerate(self._destinations):
            # TODO: Add noise model (possibly custom) to the Quantum Channels
            channel: QuantumChannel = QuantumChannel(f"QC_Source->Node{index}", delay=100, length=self._channels_length)

            self._quantum_channels.append(channel)
            port_source, port_destination = self.network.add_connection(self._source, destination, channel_to=channel,
                                                                        label=f"C_Source->Node{index + 1}")
            self._quantum_channels_port_pairs.append(PortPair(port_source, port_destination))

    ###################################################################
    # PRIVATE METHODS TO CONNECT AND DISCONNECT DESTINATION NODE PORT #
    ###################################################################

    def _connect_source_to_destination(self, n: int):
        """
        Given the number of a node, connect it to the source's quantum source component.

        :param n: The number of the node to connect
        :raises: AssertionError If the index of the node is not in the range [1, self._destinations_n]
        :raises: Exception If both of the ports are already connected to a node
        """
        assert (1 <= n <= self._destinations_n)

        source: node = self._source
        destination: node = self._destinations[n - 1]
        port_pair: PortPair = self._quantum_channels_port_pairs[n - 1]
        source_ports: dict = source.subcomponents["QuantumSource"].ports

        # Check if both the ports are already connected to a node
        if len(source_ports["qout0"].forwarded_ports) != 0 and len(source_ports["qout1"].forwarded_ports) != 0:
            raise Exception("Two nodes have already been connected to the source's QuantumSource component")

        port_n = 0 if len(source_ports["qout0"].forwarded_ports) == 0 else 1

        source.subcomponents["QuantumSource"].ports[f"qout{port_n}"].forward_output(source.ports[port_pair.source])
        destination.ports[port_pair.destination].forward_input(destination.qmemory.ports["qin0"])

    def _disconnect_source_from_destination(self, n: int):
        """
        Given the number of a node, disconnect it from the source's quantum source component.

        :param n: The number of the node to disconnect
        :raises: AssertionError If the index of the node is not in the range [1, self._destinations_n]
        :raises: Exception If the given node is not connected to the source's quantum source component
        """
        assert (1 <= n <= self._destinations_n)

        ports: dict = self._source.subcomponents["QuantumSource"].ports
        q0: dict = ports["qout0"].forwarded_ports
        q1: dict = ports["qout1"].forwarded_ports

        # Look for the node n and disconnect it. If not found, raise an exception
        if len(q0) != 0 and q0["output"].name == f"conn|{n}|C_Source->Node{n}":
            ports["qout0"].disconnect()
        elif len(q1) != 0 and q1["output"].name == f"conn|{n}|C_Source->Node{n}":
            ports["qout1"].disconnect()
        else:
            raise Exception(f"The source node is not connected to Node {n}")

    ############################################
    # GENERATE ENTANGLEMENT BETWEEN NODE PAIRS #
    ############################################

    def entangle_nodes(self, node1: int, node2: int) -> dict:
        """
        Given two node indices, generate a bell pair and send one qubit to `node1` and one qubit to `node2`. The
        function then returns the two qubits and the fidelity of their entanglement compared to the entangled state
        `|00> + |11>`.

        :param node1: The index of the first node
        :param node2: The index of the second node
        :raises: AssertionError If the index of one of the nodes is either smaller than 0 or bigger than
                 `self._destinations_n`
        :return: A dictionary containing the two qubits and the fidelity of their entanglement
        """
        assert (1 <= node1 <= self._destinations_n and 1 <= node2 <= self._destinations_n)

        # Connect the source to the nodes
        self._connect_source_to_destination(node1)
        self._connect_source_to_destination(node2)

        # Initialize and start the protocols
        protocol_source: GenerateEntanglement = GenerateEntanglement(on_node=self._network.subcomponents["Source"],
                                                                     is_source=True, name="ProtocolSource")
        protocol_node1: GenerateEntanglement = GenerateEntanglement(on_node=self._network.subcomponents[f"Node{node1}"],
                                                                    is_source=False, name=f"ProtocolNode{node1}")
        protocol_node2: GenerateEntanglement = GenerateEntanglement(on_node=self._network.subcomponents[f"Node{node2}"],
                                                                    is_source=False, name=f"ProtocolNode{node2}")

        protocol_source.start()
        protocol_node1.start()
        protocol_node2.start()

        # Run the simulation
        sim_run()

        # Disconnect the source from the nodes
        self._disconnect_source_from_destination(node1)
        self._disconnect_source_from_destination(node2)

        # Read the destination's memory
        qubit_node1, = self._network.subcomponents[f"Node{node1}"].qmemory.peek(0)
        qubit_node2, = self._network.subcomponents[f"Node{node2}"].qmemory.peek(0)
        entanglement_fidelity: float = qubits.fidelity([qubit_node1, qubit_node2], b00)

        return {"qubits": (qubit_node1, qubit_node2), "fidelity": entanglement_fidelity}
