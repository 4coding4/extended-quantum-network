from netsquid import sim_run, sim_time
from netsquid.components import QuantumChannel
from netsquid.components.qmemory import MemPositionEmptyError, Qubit
from netsquid.nodes import Network, node
from typing import List, Dict, Union, Tuple

from src.helper.error.error import error_exit
from src.helper.network.MemorySnapshot import MemorySnapshot
from src.helper.network.PortPair import PortPair
from src.helper.network.Factory.QuantumChannel import QuantumChannelFactory
from src.helper.network.Factory.QuantumProcessor import QuantumProcessorFactory
from src.helper.network.Factory.QuantumSource import QuantumSourceFactory
from src.helper.network.entanglement_swapping import apply_gates, \
    perform_and_get_bell_measurement_w_state, get_results_qubits
from src.protocols.GenerateEntanglement import GenerateEntanglement


class StarNetwork:
    """
    Class to create a star network topology. The center of the network is composed of a Node with only a Quantum Source
    as a component. All the other nodes are composed by quantum processors, and are connected to the source node by
    means of quantum connections. One of the points of the stars is a repeater, which is connected to another node.


    Default network topology
    ------------------------
                 +-----+
                 | N1  |
                 +-----+
                    ^
                    |
                   QC1
                    |
    +----+        +---+        +---+        +-----+
    | N2 | <-QC2- | S | -QC4-> | R | <-QC5- | RN4 |
    +----+        +---+        +---+        +-----+
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
        - Quantum Source (generates |00> + |11>)

    R:
        - Quantum Processor
        - Quantum Memory (2x memory positions)

    Ni:
        - Quantum Processor
        - Quantum Memory (1x memory position)

    RNi:
        - Quantum Source (generates |00> + |11>)
        - Quantum Processor
        - Quantum Memory (1x memory position)


    Channels
    --------
    QCi:
        - Unidirectional Quantum Channel (S -> [Ni | R])

    QC5:
        - Unidirectional Quantum Channel (S <- RN)


    Network properties
    ------------------
    destinations_n (default: 5):
        The number of destination nodes in the network (one of which is a repeater)

    source_delay (default: 1e5):
        Delay of the delay model of the quantum source in nanoseconds

    channels_length (default: 10):
        The length of the quantum channels in km

    node_mem_positions (default: 1):
        The memory positions of the node's quantum memories

    repeater_mem_positions (default: 2):
        The memory positions of the repeater's quantum memory
    """
    _channels_length: float = 1

    def __init__(self, models: dict = None, lengths: float = _channels_length):
        """
        Constructor for the StarNetwork class.
        """
        self._models: dict
        self._destinations_n: int = 5
        self._source_delay: float = 1e5
        # self._channels_length: float = 1
        self._node_mem_positions: int = 1
        self._repeater_mem_positions: int = 4
        self._source_num_ports: int = 4
        self._remote_source_num_ports: int = 4
        self._remote_node_mem_positions: int = 2

        # Network object and network components
        self._network: Network = Network("StarNetwork")

        self._source: node = None
        self._destinations: [node] = []

        self._quantum_channels: [QuantumChannel] = []
        self._quantum_channels_port_pairs: [PortPair] = []

        self._models = models
        self._channels_length = lengths

        self._init_source()
        self._init_destinations()
        self._init_quantum_channels()
        self._connect_remote_node()

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

    @property
    def channels_length(self) -> float:
        """
        :type: float
        """
        return self._channels_length

    @property
    def models(self) -> dict:
        """
        :type: dict
        """
        return self._models

    @property
    def repeater_mem_positions(self) -> int:
        """
        :type: int
        """
        return self._repeater_mem_positions

    @property
    def node_mem_positions(self) -> int:
        """
        :type: int
        """
        return self._node_mem_positions

    @property
    def remote_node_mem_positions(self) -> int:
        """
        :type: int
        """
        return self._remote_node_mem_positions

    ###########

    # SETTERS #
    ###########

    @source_delay.setter
    def source_delay(self, ns: float):
        """
        Set the source delay in nanoseconds (ns).

        :param ns: The amount of nanoseconds
        :raises AssertionError: If ns is 0.0 or less
        """
        assert (ns >= 0.0)
        self._source_delay = ns

    @destinations_n.setter
    def destinations_n(self, n: int):
        """
        Set the number of destination nodes in the network.

        :param n: The number of nodes
        :raises AssertionError: If n is 0 or less
        """
        assert (n > 0.0)
        self._destinations_n = n

    @channels_length.setter
    def channels_length(self, n: float):
        """
        Set the number of channel length in the network.

        :param n: The channel length (in meters)
        :raises AssertionError: If n is 0 or less
        """
        assert (n > 0)

        self._channels_length = n / 1000
        self._change_lengths(self._channels_length)

    @models.setter
    def models(self, models_dict: dict):
        """
        Set the dictionary of the models for the quantum channels.
        :param models_dict: The dictionary of models
        """
        self._models = models_dict

    #############################################
    # PRIVATE HELPERS USED TO BUILD THE NETWORK #
    #############################################

    def _init_source(self):
        """
        Initialize the source node of the network.
        """
        quantum_source_factory = QuantumSourceFactory(self._source_delay, self._source_num_ports / 2)

        self._source = self._network.add_node("Source")
        self._source.add_subcomponent(
            quantum_source_factory.get("QuantumSource")
        )
        self._source.add_subcomponent(
            quantum_source_factory.get("QuantumSource1")
        )

    def _init_destinations(self):
        """
        Initialize the destination nodes of the network.
        """
        quantum_source_factory = QuantumSourceFactory(self._source_delay, self._remote_source_num_ports / 2)
        quantum_processor_factory = QuantumProcessorFactory()

        for destination_n in range(1, self._destinations_n + 1):
            if destination_n == self._destinations_n - 1:
                # Initialization of the repeater
                self._destinations.append(self._network.add_node("Repeater"))
                self._destinations[destination_n - 1].add_subcomponent(
                    quantum_processor_factory.get("QP_Repeater", self._repeater_mem_positions)
                )
            elif destination_n == self._destinations_n:
                # Initialize the remote node
                self._destinations.append(self._network.add_node("RemoteNode"))
                self._destinations[destination_n - 1].add_subcomponent(
                    quantum_processor_factory.get("QP_RemoteNode", self._remote_node_mem_positions)
                )
                self._destinations[destination_n - 1].add_subcomponent(
                    quantum_source_factory.get("RemoteQuantumSource")
                )
                self._destinations[destination_n - 1].add_subcomponent(
                    quantum_source_factory.get("RemoteQuantumSource1")
                )
            else:
                # Initialize normal nodes
                self._destinations.append(self._network.add_node(f"Node{destination_n}"))
                self._destinations[destination_n - 1].add_subcomponent(
                    quantum_processor_factory.get(f"QP_Node{destination_n}", self._node_mem_positions)
                )

    def _init_quantum_channels(self, length: float = _channels_length):
        """
        Initialize the quantum channels of the network.
        """
        self._quantum_channels.clear()
        quantum_channel_factory = QuantumChannelFactory(length, self._models)
        repeater = self._network.subcomponents["Repeater"]

        for (index, destination) in enumerate(self._destinations):
            if index == self._destinations_n - 2:
                # Initialize quantum channel for the repeater
                name = "C_Source->Repeater"
                channel: QuantumChannel = quantum_channel_factory.get(name)
                self._quantum_channels.append(channel)

                port_source, port_repeater = self.network.add_connection(self._source, destination,
                                                                         channel_to=channel,
                                                                         label=name)
                self._quantum_channels_port_pairs.append(PortPair(port_source, port_repeater, name))
                # second quantum channel for the repeater
                name1 = "C_Source1->Repeater"
                channel1: QuantumChannel = quantum_channel_factory.get(name1)
                self._quantum_channels.append(channel1)

                port_source1, port_repeater1 = self.network.add_connection(self._source, destination,
                                                                           channel_to=channel1,
                                                                           label=name1)
                self._quantum_channels_port_pairs.append(PortPair(port_source1, port_repeater1, name1))
            elif index == self._destinations_n - 1:
                # Initialize quantum channel for the remote node
                name = "C_RemoteNode->Repeater"
                channel: QuantumChannel = quantum_channel_factory.get(name)
                self._quantum_channels.append(channel)

                port_remote, port_repeater = self.network.add_connection(destination, repeater,
                                                                         channel_to=channel,
                                                                         label=name)
                self._quantum_channels_port_pairs.append(PortPair(port_remote, port_repeater, name))
                # second quantum channel for the remote node
                name1 = "C_RemoteNode1->Repeater"
                channel1: QuantumChannel = quantum_channel_factory.get(name1)
                self._quantum_channels.append(channel1)

                port_remote1, port_repeater1 = self.network.add_connection(destination, repeater, channel_to=channel1,
                                                                           label=name1)
                self._quantum_channels_port_pairs.append(PortPair(port_remote1, port_repeater1, name1))
            else:
                # Initialize quantum channels for normal nodes
                mid_name = "C_Source->Node"
                channel: QuantumChannel = quantum_channel_factory.get(mid_name + str(index))
                self._quantum_channels.append(channel)
                pair_name = mid_name + str(index + 1)
                port_source, port_destination = self.network.add_connection(self._source, destination,
                                                                            channel_to=channel,
                                                                            label=pair_name)
                self._quantum_channels_port_pairs.append(
                    PortPair(port_source, port_destination, pair_name))

    ###################################################################
    # PRIVATE METHODS TO CONNECT AND DISCONNECT DESTINATION NODE PORT #
    ###################################################################

    def select_source(self, channel_n) -> str:
        """
        Given the index of a quantum channel, select the source for the destination node.

        :param channel_n: The index of the quantum channel
        :return: The selected source_name for the destination node
        """
        selected_source_name = "QuantumSource"
        if channel_n == 0:
            return selected_source_name
        else:
            return selected_source_name + str(channel_n)

    def get_port_n_in(self, source_ports, component_name) -> int:
        """
        Given the source_ports of the node, return the index of the input port for the node.

        :param source_ports: The source ports of the node
        :param component_name: The name of the QuantumSource component
        :return: The index of the input port for the node
        """
        # can only be 0 or 1
        if len(source_ports["qout0"].forwarded_ports) == 0:
            port_n = 0
        elif len(source_ports["qout1"].forwarded_ports) == 0:
            port_n = 1
        else:
            error_exit("get_port_n_in: Two nodes have already been connected to the "
                       "source's QuantumSource component called: " + component_name)

        return port_n

    def get_port_n_out(self, n: int, channel_n: int) -> int:
        """
        Given the number of a node and the index of a quantum channel, return the index of the output port for the node.

        :param n: The number of the node
        :param channel_n: The index of the quantum channel
        :return: The index of the output port for the node
        """
        if n == self._destinations_n - 1:  # remote node
            if channel_n == 0:
                port_n_out = 0
            else:
                port_n_out = 2
        elif n == self._destinations_n - 2:  # repeater
            port_n_out = 1
        else:
            port_n_out = 0

        return port_n_out

    def _connect_source_to_destination(self, n: int, channel_n=0):
        """
        Given the number of a node, connect it to the source's quantum source component.

        :param n: The number of the node to connect
        :raises AssertionError: If the index of the node is not in the range [1, self._destinations_n - 1]
        :raises Exception: If both of the ports are already connected to a node
        """
        assert (1 <= n <= self._destinations_n - 1)

        source: node = self._source
        destination: node = self._destinations[n - 1]
        port_pair: PortPair = self._quantum_channels_port_pairs[n - 1]
        component_name = self.select_source(channel_n)
        source_ports: dict = source.subcomponents[component_name].ports

        # Check if both the ports are already connected to a node
        if len(source_ports["qout0"].forwarded_ports) != 0 and len(source_ports["qout1"].forwarded_ports) != 0:
            error_exit("_connect_source_to_destination: Two nodes have already been connected to the "
                       "source's QuantumSource component called: " + component_name)

        port_n = self.get_port_n_in(source_ports, component_name)

        source_ports[f"qout{port_n}"].forward_output(source.ports[port_pair.source])

        port_n_out = self.get_port_n_out(n, channel_n)

        destination.ports[port_pair.destination].forward_input(destination.qmemory.ports[f"qin{port_n_out}"])

    def _disconnect_source_from_destination(self, n: int):
        """
        Given the number of a node, disconnect it from the source's quantum source component.

        :param n: The number of the node to disconnect
        :raises AssertionError: If the index of the node is not in the range [1, self._destinations_n - 1]
        :raises Exception: If the given node is not connected to the source's quantum source component
        """
        assert (1 <= n <= self._destinations_n - 1)

        ports: dict = self._source.subcomponents["QuantumSource"].ports
        q0: dict = ports["qout0"].forwarded_ports
        q1: dict = ports["qout1"].forwarded_ports

        ports1: dict = self._source.subcomponents["QuantumSource1"].ports
        q01: dict = ports1["qout0"].forwarded_ports
        q11: dict = ports1["qout1"].forwarded_ports

        # Look for the node n and disconnect it. If not found, raises an exception
        if len(q0) != 0 and (q0["output"].name == f"conn|{n}|C_Source->Node{n}"
                             or q0["output"].name == f"conn|{n}|C_Source->Repeater"):
            ports["qout0"].disconnect()
        elif len(q1) != 0 and (q1["output"].name == f"conn|{n}|C_Source->Node{n}"
                               or q1["output"].name == f"conn|{n}|C_Source->Repeater"):
            ports["qout1"].disconnect()
        elif len(q01) != 0 and (q01["output"].name == f"conn|{n}|C_Source->Node{n}"
                                or q01["output"].name == f"conn|{n}|C_Source->Repeater"):
            ports1["qout0"].disconnect()
        elif len(q11) != 0 and (q11["output"].name == f"conn|{n}|C_Source->Node{n}"
                                or q11["output"].name == f"conn|{n}|C_Source->Repeater"):
            ports1["qout1"].disconnect()
        else:
            error_exit(f"The source node is not connected to Node {n}")

    def _connect_remote_node(self):
        """
        Connect the remote node ports to the quantum repeater.
        """
        repeater: node = self._destinations[-2]
        remote_node: node = self._destinations[-1]
        port_pair: PortPair = self._quantum_channels_port_pairs[-2]
        port_pair1: PortPair = self._quantum_channels_port_pairs[-1]

        remote_node.subcomponents["RemoteQuantumSource"].ports["qout0"].forward_output(
            remote_node.ports[port_pair.source])
        remote_node.subcomponents["RemoteQuantumSource"].ports["qout1"].connect(remote_node.qmemory.ports["qin0"])

        repeater.ports[port_pair.destination].forward_input(repeater.qmemory.ports["qin1"])

        # second quantum channel for the remote node
        remote_node.subcomponents["RemoteQuantumSource1"].ports["qout0"].forward_output(
            remote_node.ports[port_pair1.source])
        remote_node.subcomponents["RemoteQuantumSource1"].ports["qout1"].connect(remote_node.qmemory.ports["qin1"])

        repeater.ports[port_pair1.destination].forward_input(repeater.qmemory.ports["qin3"])

    def _change_lengths(self, new_length: float):
        """
        Change the lengths of the quantum channels

        :param new_length:
        :return:
        """
        assert (new_length >= 0)

        if new_length == self._channels_length:
            return

        self._init_quantum_channels(new_length)

    ############################################
    # GENERATE ENTANGLEMENT BETWEEN NODE PAIRS #
    ############################################

    def protocol_a(self, node1: int = 1, node2: int = 2, node3: int = 4, debug: bool = False):
        """
        Perform the steps of entangling 3 nodes given their indices
        (similarly to entangle_nodes but with limited customization).

        :param node1: The index of the first node, default is 1
        :param node2: The index of the second node, default is 2
        :param node3: The index of the third node (Remote Node), default is 4
        :param debug: If True, print the memory positions, before the entanglement swapping (default is False)
        :raises AssertionError: If either `node1`, `node2`, or `node3` is not between 1 and `self._destinations_n - 1`,
        and one of the nodes is the same as the other,
        and `node1` is greater than `node2` and `node2` is greater than `node3`
        :return: A dictionary containing the qubits and their fidelity
        """
        assert (1 <= node1 <= self._destinations_n - 1
                and 1 <= node2 <= self._destinations_n - 1
                and 1 <= node3 <= self._destinations_n - 1
                and node1 < node2 < node3
                and node1 != node2 != node3)

        tot_num_channels = self._repeater_mem_positions // 2  # 2 memories per channel for the repeater
        assert tot_num_channels == 2

        # define memory_snapshot class
        memory_snapshot = MemorySnapshot(self._network, node1, node2, node3,
                                         self.repeater_mem_positions,
                                         self.node_mem_positions,
                                         self.remote_node_mem_positions)

        channels_n = [i for i in range(0, tot_num_channels)][::-1]  # reverse the list to start from the last channel

        for i, channel_n in enumerate(channels_n):
            first_node = node1 if i == 0 else node2

            # this way uses only 1 mem position0 and 1 qchannel between nodes
            self._perform_entanglement(first_node, node3, channel_n)

            if debug:
                expected_output = "4 Qubits and 4 None" if i == 0 else "all Qubits and 0 None"
                extra_msg = "" if i == 0 else " and Before entanglement swapping"

                memory_snapshot.show_all_memory_positions(
                    initial_msg=f"After entanglement in nodes {first_node}-3{extra_msg}:",
                    end_msg=expected_output)

        results = self.entanglement_swapping([node1, node2, node3], debug)

        if debug:
            expected_output = "all None"
            memory_snapshot.show_all_memory_positions(
                initial_msg="After entanglement swapping:",
                end_msg=expected_output)

        return results

    def entangle_nodes(self, node1: int = 1, node2: int = 4, debug: bool = False):
        """
        Perform the steps of entangling two nodes given their indices.

        :param node1: The index of the first node (default is 1)
        :param node2: The index of the second node (default is 4, the Remote Node)
        :param debug: If True, print the memory positions, before the entanglement swapping (default is False)
        :raises AssertionError: If either `node1` or `node2` is not between 1 and `self._destinations_n - 1` and `node1`
                                and `node2` are the same node
        :return: A dictionary containing the qubits and their fidelity
        """
        assert (1 <= node1 <= self._destinations_n - 1 and 1 <= node2 <= self._destinations_n - 1 and node1 != node2)

        self._perform_entanglement(node1, node2)
        return self.entanglement_swapping([node1, node2], debug)

    def _perform_entanglement(self, node1: int, node2: int, channel_n=0):
        """
        Given two node indices, generate a bell pair and send one qubit to `node1` and one qubit to `node2`. The
        function then returns the two qubits and the fidelity of their entanglement compared to the entangled state
        `|00> + |11>`.

        :param node1: The index of the first node
        :param node2: The index of the second node
        """
        protocol_node1: GenerateEntanglement
        protocol_node2: GenerateEntanglement

        # Connect the source to the nodes
        self._connect_source_to_destination(node1, channel_n)
        self._connect_source_to_destination(node2, channel_n)

        # select the sources that should be connected to the quantum channels and generate entanglement
        channel_n_str = "" if channel_n == 0 else str(channel_n)
        source_name = "QuantumSource" + channel_n_str
        remote_source_name = "Remote" + source_name

        # Initialize and start the protocols
        protocol_source: GenerateEntanglement = GenerateEntanglement(on_node=self._network.subcomponents["Source"],
                                                                     is_source=True, name="ProtocolSource",
                                                                     qsource_name=source_name)

        if node1 == self._destinations_n - 1 or node2 == self._destinations_n - 1:
            protocol_remote = GenerateEntanglement(on_node=self._network.subcomponents["RemoteNode"],
                                                   is_remote=True, name="ProtocolRemote",
                                                   qsource_name=remote_source_name)

            protocol_repeater = GenerateEntanglement(on_node=self._network.subcomponents["Repeater"],
                                                     is_repeater=True, name="ProtocolRepeater")

            if node1 == self._destinations_n - 1:
                protocol_node1 = protocol_repeater
                protocol_node2 = GenerateEntanglement(on_node=self._network.subcomponents[f"Node{node2}"],
                                                      name=f"ProtocolNode{node2}")
            elif node2 == self._destinations_n - 1:
                protocol_node1 = GenerateEntanglement(on_node=self._network.subcomponents[f"Node{node1}"],
                                                      name=f"ProtocolNode{node1}")
                protocol_node2 = protocol_repeater

            protocol_remote.start()
        else:
            protocol_node1 = GenerateEntanglement(on_node=self._network.subcomponents[f"Node{node1}"],
                                                  name=f"ProtocolNode{node1}")
            protocol_node2 = GenerateEntanglement(on_node=self._network.subcomponents[f"Node{node2}"],
                                                  name=f"ProtocolNode{node2}")

        protocol_source.start()
        protocol_node1.start()
        protocol_node2.start()

        # Run the simulation
        sim_run()
        print(f"Entanglement simulation run in {sim_time()} nanoseconds")

        # Disconnect the source from the nodes
        self._disconnect_source_from_destination(node1)
        self._disconnect_source_from_destination(node2)

    def get_entanglement_swapping_parameters(self, nodes) -> Tuple[List[List[int]], List[int], List[int], int]:
        l = len(nodes)
        if l == 2:
            m_mem_positions = [[]]
            positions = [-1]
            nodes_list = nodes
            mem_positions = [0, 0]
            repeater_memory_positions = 2
        elif l == 3:
            m_mem_positions = [[0, 1], [2, 3]]
            positions = [0, 1]
            nodes_list = nodes
            nodes_list.append(nodes_list[-1]) # the last element again
            mem_positions = [0, 0, 0, 1]  # 1 because "RemoteNode" has 2 mem positions
            repeater_memory_positions = 4
        else:
            error_exit("Invalid number of nodes for entanglement swapping")

        return m_mem_positions, positions, nodes_list, mem_positions, repeater_memory_positions

    def get_bell_states(self, m_mem_positions: List[List[int]], debug: bool) -> List[int]:
        repeater_memory = self._network.subcomponents["Repeater"].qmemory
        states = []
        for m_mem_position_pair in m_mem_positions:
            _, state = perform_and_get_bell_measurement_w_state(repeater_memory, m_mem_position_pair, debug)
            states.append(state)
        return states

    def try_discard_mem_positions_repeater(self, repeater_memory, repeater_memory_positions: int) -> None:
        for i in range(repeater_memory_positions):
            try:
                repeater_memory.discard(i)
            except MemPositionEmptyError:
                pass

    def entanglement_swapping(self, nodes: List[int], debug: bool = False) \
            -> List[Dict[str, Union[List[Qubit], float, bool]]]:
        """
        Given 2 or 3 nodes, perform entanglement swapping only if 1 of the nodes is the Repeater.

        :param nodes: The  nodes, where the last one is the Remote Node
        :param debug: If True, print the memory positions, before the entanglement swapping (default is False)
        :return: A dictionary containing the qubits and their fidelity (list of dictionaries)
        """
        l = len(nodes)
        m_mem_positions, positions, nodes_list, mem_positions, repeater_memory_positions = \
            self.get_entanglement_swapping_parameters(nodes)

        repeater_memory = self._network.subcomponents["Repeater"].qmemory
        remote_node_memory = self._network.subcomponents["RemoteNode"].qmemory
        try:
            if any(single_node == self._destinations_n - 1 for single_node in nodes):
                if debug:
                    print('entanglement_swapping with #nodes:' + str(l))
                states = self.get_bell_states(m_mem_positions, debug)

                # swap the qubits in memory position 0 and 1,
                # and then apply the necessary gates
                # then do the same for the position 2 and 3

                # check that len(states) ==  len(positions)
                if len(states)!= len(positions):
                    error_exit("Mismatch length between states and positions in entanglement swapping")
                # apply gates for first and second state/position for l=3 otherwise -1
                for i in range(len(states)):
                    state = states[i]
                    position = positions[i]
                    apply_gates(state, remote_node_memory, position, debug)

        except MemPositionEmptyError as e:
            print(e)

        try:
            labels = [f"Node{node_n}" if node_n != self._destinations_n - 1 else "RemoteNode"
                      for node_n in nodes_list]  # the last 2 are always "RemoteNode" if l=3 otherwise only the last one is always "RemoteNode"
            # pop the qubits from the memory positions in the nodes specified by the labels (none repeater) & positions
            qubits = [self._network.subcomponents[label].qmemory.pop(mem_pos)[0]
                      for label, mem_pos in zip(labels, mem_positions)]
            # peak in all the repeater memory positions, from 0 to 3 (both included)
            for i in range(repeater_memory_positions):
                _, = repeater_memory.peek(i)

            results = get_results_qubits(qubits)
            # try to discard the memory positions in the repeater
            if labels[-1] == "RemoteNode":  # same as node3_label: "RemoteNode"
                # list of the memory positions from 0 to 3 (both included)
                self.try_discard_mem_positions_repeater(repeater_memory, mem_positions)
        except (ValueError, AttributeError) as e:
            print(e)
            results = {"message": "Some Qubits were lost during transfer", "error": True}
        return results
