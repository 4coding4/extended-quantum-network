from netsquid.components import QuantumChannel, QSource, SourceStatus, FixedDelayModel, QuantumProcessor
from netsquid.nodes import Network, node
from netsquid.qubits import StateSampler, ketstates

from src.network.PortPair import PortPair


class StarNetwork:
    # Network properties
    _destinations_n: int = 4
    _source_delay: float = 5.0
    _channels_length: int = 10

    # Network and network components
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
        assert(ns >= 0.0)
        self._source_delay = ns

    @destinations_n.setter
    def destinations_n(self, n: int):
        """
        Set the number of destination nodes in the network.

        :param n: The number of nodes
        :raise: AssertionError If n is 0 or less
        """
        assert(n > 0)
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
        for destination_n in range(1, self._destinations_n+1):
            self._destinations.append(self._network.add_node(f"Node{destination_n}"))
            self._destinations[destination_n-1].add_subcomponent(
                QuantumProcessor(f"QP_Node{destination_n}", num_positions=3, fallback_to_nonphysical=True)
            )

    def _init_quantum_channels(self):
        """
        Initialize the quantum channels of the network.
        """
        for (index, destination) in enumerate(self._destinations):
            channel: QuantumChannel = QuantumChannel(f"QC_Source->Node{index}", delay=100, length=self._channels_length)

            self._quantum_channels.append(channel)
            port_source, port_destination = self.network.add_connection(self._source, destination, channel_to=channel,
                                                                        label=f"C_Source->Node{index+1}")
            self._quantum_channels_port_pairs.append(PortPair(port_source, port_destination))

    #####################################################################
    # PRIVATE METHODS TO CONNECT AND DISCONNECT DESTINATION NODES PORTS #
    #####################################################################

    def _connect_source_to_destination(self, n: int):
        """
        Given the number of a node, connect it to the source's quantum source component.

        :param n: The number of the node to connect
        :raises: AssertionError If the index of the node is not in the range [1, self._destinations_n]
        :raises: Exception If both of the ports are already connected to a node
        """
        assert(1 < n <= self._destinations_n)

        source: node = self._source
        destination: node = self._destinations[n-1]
        port_pair: PortPair = self._quantum_channels_port_pairs[n-1]
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
        assert(1 < n <= self._destinations_n)

        ports: dict = self._source.subcomponents["QuantumSource"].ports
        q0: dict = ports["qout0"].forwarded_ports
        q1: dict = ports["qout1"].forwarded_ports

        if len(q0) != 0 and q0["output"].name == f"conn|{n}|C_Source->Node{n}":
            ports["qout0"].disconnect()
        elif len(q1) != 0 and q1["output"].name == f"conn|{n}|C_Source->Node{n}":
            ports["qout1"].disconnect()
        else:
            raise Exception(f"The source node is not connected to Node {n}")
