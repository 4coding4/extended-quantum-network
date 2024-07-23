from netsquid import sim_run, qubits, b00, sim_time
from netsquid.components import QuantumChannel, INSTR_MEASURE_BELL, INSTR_Z, INSTR_X
from netsquid.components.qmemory import MemPositionEmptyError, Qubit
from netsquid.nodes import Network, node
from netsquid.qubits import QRepr
from typing import Tuple, List, Dict, Union

from src.network.MemorySnapshot import MemorySnapshot
from src.network.PortPair import PortPair
from src.network.QuantumComponents import QuantumComponents as QC
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
    _models: dict = None
    _destinations_n: int = 5
    _source_delay: float = 1e5
    _channels_length: float = 1
    _node_mem_positions: int = 1
    _repeater_mem_positions: int = 4
    _source_num_ports: int = 4
    _remote_source_num_ports: int = 4
    _remote_node_mem_positions: int = 2

    # Network object and network components
    _network: Network = Network("StarNetwork")

    _source: node = None
    _destinations: [node] = []

    _quantum_channels: [QuantumChannel] = []
    _quantum_channels_port_pairs: [PortPair] = []

    def __init__(self, models: dict = None, lengths: float = _channels_length):
        """
        Constructor for the StarNetwork class.
        """
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
        self._source = self._network.add_node("Source")
        self._source.add_subcomponent(
            QC.get_source("QuantumSource", self._source_delay, self._source_num_ports / 2)
        )
        self._source.add_subcomponent(
            QC.get_source("QuantumSource1", self._source_delay, self._source_num_ports / 2)
        )

    def _init_destinations(self):
        """
        Initialize the destination nodes of the network.
        """
        for destination_n in range(1, self._destinations_n + 1):
            if destination_n == self._destinations_n - 1:
                # Initialization of the repeater
                self._destinations.append(self._network.add_node(f"Repeater"))
                self._destinations[destination_n - 1].add_subcomponent(
                    QC.get_processor(f"QP_Repeater", self._repeater_mem_positions)
                )
            elif destination_n == self._destinations_n:
                # Initialize the remote node
                self._destinations.append(self._network.add_node(f"RemoteNode"))
                self._destinations[destination_n - 1].add_subcomponent(
                    QC.get_processor(f"QP_RemoteNode", self._remote_node_mem_positions)
                )
                self._destinations[destination_n - 1].add_subcomponent(
                    QC.get_source("RemoteQuantumSource", self._source_delay, self._remote_source_num_ports / 2)
                )
                self._destinations[destination_n - 1].add_subcomponent(
                    QC.get_source("RemoteQuantumSource1", self._source_delay, self._remote_source_num_ports / 2)
                )
            else:
                # Initialize normal nodes
                self._destinations.append(self._network.add_node(f"Node{destination_n}"))
                self._destinations[destination_n - 1].add_subcomponent(
                    QC.get_processor(f"QP_Node{destination_n}", self._node_mem_positions)
                )

    def _init_quantum_channels(self, length: float = _channels_length):
        """
        Initialize the quantum channels of the network.
        """
        self._quantum_channels.clear()

        for (index, destination) in enumerate(self._destinations):
            if index == self._destinations_n - 2:
                # Initialize quantum channel for the repeater
                channel: QuantumChannel = QuantumChannel(f"QC_Source->Repeater", length=length,
                                                         models=self._models)
                self._quantum_channels.append(channel)

                port_source, port_repeater = self.network.add_connection(self._source, destination, channel_to=channel,
                                                                         label=f"C_Source->Repeater")
                self._quantum_channels_port_pairs.append(PortPair(port_source, port_repeater, f"C_Source->Repeater"))
                # second quantum channel for the repeater
                channel1: QuantumChannel = QuantumChannel(f"QC_Source1->Repeater", length=length,
                                                          models=self._models)
                self._quantum_channels.append(channel1)

                port_source1, port_repeater1 = self.network.add_connection(self._source, destination,
                                                                           channel_to=channel1,
                                                                           label=f"C_Source1->Repeater")
                self._quantum_channels_port_pairs.append(PortPair(port_source1, port_repeater1, f"C_Source1->Repeater"))
            elif index == self._destinations_n - 1:
                # Initialize quantum channel for the remote node
                channel: QuantumChannel = QuantumChannel(f"QC_RemoteNode->Repeater", length=length,
                                                         models=self._models)
                self._quantum_channels.append(channel)

                repeater = self._network.subcomponents["Repeater"]
                port_remote, port_repeater = self.network.add_connection(destination, repeater, channel_to=channel,
                                                                         label=f"C_RemoteNode->Repeater")
                self._quantum_channels_port_pairs.append(
                    PortPair(port_remote, port_repeater, f"C_RemoteNode->Repeater"))
                # second quantum channel for the remote node
                channel1: QuantumChannel = QuantumChannel(f"QC_RemoteNode1->Repeater", length=length,
                                                          models=self._models)
                self._quantum_channels.append(channel1)

                # repeater = self._network.subcomponents["Repeater"]
                port_remote1, port_repeater1 = self.network.add_connection(destination, repeater, channel_to=channel1,
                                                                           label=f"C_RemoteNode1->Repeater")
                self._quantum_channels_port_pairs.append(
                    PortPair(port_remote1, port_repeater1, f"C_RemoteNode1->Repeater"))
            else:
                # Initialize quantum channels for normal nodes
                channel: QuantumChannel = QuantumChannel(f"QC_Source->Node{index}", length=length,
                                                         models=self._models)
                self._quantum_channels.append(channel)

                port_source, port_destination = self.network.add_connection(self._source, destination,
                                                                            channel_to=channel,
                                                                            label=f"C_Source->Node{index + 1}")
                self._quantum_channels_port_pairs.append(
                    PortPair(port_source, port_destination, f"C_Source->Node{index + 1}"))

    ###################################################################
    # PRIVATE METHODS TO CONNECT AND DISCONNECT DESTINATION NODE PORT #
    ###################################################################

    def _connect_source_to_destination(self, n: int,
                                       channel_n=0):  # TODO cognitive complexity is too high (sonarlint max is 15, this 16), reduce by extrapolating the logic to a helper function
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
        source_ports: dict = source.subcomponents["QuantumSource"].ports
        source_ports1: dict = source.subcomponents["QuantumSource1"].ports

        # Check if both the ports are already connected to a node
        if len(source_ports["qout0"].forwarded_ports) != 0 and len(source_ports["qout1"].forwarded_ports) != 0:
            if len(source_ports1["qout0"].forwarded_ports) != 0 and len(source_ports1["qout1"].forwarded_ports) != 0:
                raise Exception("Two nodes have already been connected to the source's QuantumSource component")

        # TODO REFACTOR THIS
        if len(source_ports["qout0"].forwarded_ports) == 0:
            port_n = 0
            selected_source_ports = source_ports
            component_name = "QuantumSource"
        elif len(source_ports["qout1"].forwarded_ports) == 0:
            port_n = 1
            selected_source_ports = source_ports
            component_name = "QuantumSource"
        elif len(source_ports1["qout0"].forwarded_ports) == 0:
            port_n = 0
            selected_source_ports = source_ports1
            component_name = "QuantumSource1"
        elif len(source_ports1["qout1"].forwarded_ports) == 0:
            port_n = 1
            selected_source_ports = source_ports1
            component_name = "QuantumSource1"
        else:
            raise Exception("Two nodes have already been connected to the source's QuantumSource component")

        # if channel_n == 0:
        #     source_ports[f"qout{port_n}"].forward_output(source.ports[port_pair.source])
        #     destination.ports[port_pair.destination].forward_input(destination.qmemory.ports["qin0"])
        # else:
        #     source_ports1[f"qout{port_n}"].forward_output(source.ports[port_pair.source])
        #     if n == self._destinations_n - 2:  # repeater
        #         destination.ports[port_pair.destination].forward_input(destination.qmemory.ports["qin0"])
        #     else:
        #         destination.ports[port_pair.destination].forward_input(destination.qmemory.ports["qin1"])

        # old (keep it since we still need for simple cases/routing)
        source.subcomponents["QuantumSource"].ports[f"qout{port_n}"].forward_output(source.ports[port_pair.source])
        destination.ports[port_pair.destination].forward_input(destination.qmemory.ports["qin0"])

        source.subcomponents["QuantumSource1"].ports[f"qout{port_n}"].forward_output(source.ports[port_pair.source])
        if n == self._destinations_n - 1:  # remote node
            if channel_n == 0:
                destination.ports[port_pair.destination].forward_input(destination.qmemory.ports["qin0"])
            else:
                destination.ports[port_pair.destination].forward_input(destination.qmemory.ports["qin2"])
        elif n == self._destinations_n - 2:  # repeater
            destination.ports[port_pair.destination].forward_input(destination.qmemory.ports["qin1"])
        else:
            destination.ports[port_pair.destination].forward_input(destination.qmemory.ports["qin0"])

        # new
        # source.subcomponents[component_name].ports[f"qout{port_n}"].forward_output(source.ports[port_pair.source])  # enabled
        # selected_source_ports[f"qout{port_n}"].forward_output(source.ports[port_pair.source])
        # destination.ports[port_pair.destination].forward_input(destination.qmemory.ports["qin0"])  # enabled

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

        # Look for the node n and disconnect it. If not found, raises an exception
        if len(q0) != 0 and (q0["output"].name == f"conn|{n}|C_Source->Node{n}"
                             or q0["output"].name == f"conn|{n}|C_Source->Repeater"):
            ports["qout0"].disconnect()
        elif len(q1) != 0 and (q1["output"].name == f"conn|{n}|C_Source->Node{n}"
                               or q1["output"].name == f"conn|{n}|C_Source->Repeater"):
            ports["qout1"].disconnect()
        else:
            raise Exception(f"The source node is not connected to Node {n}")

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

        channels_n = []
        for i in range(0, 2):
            channels_n.append(i)
        # reverse the list to start from the last channel
        channels_n.reverse()
        for i, channel_n in enumerate(channels_n):
            if i == 0:
                first_node = node1
            elif i == 1:
                first_node = node2

            # this way uses only 1 mem position0 and 1 qchannel between nodes
            self._perform_entanglement(first_node, node3, channel_n)

            if debug:
                first_node_number = i + 1
                if i == 0:
                    expected_output = "If it is working correctly, the output should have 4 Qubits and 4 None"
                    extra_msg = ""
                elif i == 1:
                    expected_output = "If it is working correctly, the output should have all Qubits and 0 None"
                    extra_msg = " and Before entanglement swapping"

                MemorySnapshot(self._network, node1, node2, node3).show_all_memory_positions(
                    initial_msg=f"After entanglement in nodes {first_node_number}-3{extra_msg}:",
                    end_msg=expected_output)

        results = self._perform_new_entanglement_swapping(node1, node2, node3, debug)

        if debug:
            expected_output = "If it is working correctly, the output should have all None"
            MemorySnapshot(self._network, node1, node2, node3).show_all_memory_positions(
                initial_msg="After entanglement swapping:",
                end_msg=expected_output)

        return results

    def entangle_nodes(self, node1: int = 1, node2: int = 4, debug: bool = False):
        """
        Perform the steps of entangling two nodes given their indices.

        :param node1: The index of the first node (default is 1)
        :param node2: The index of the second node (default is 4, the Remote Node)
        :param debug: unused boolean (default is False)
        :raises AssertionError: If either `node1` or `node2` is not between 1 and `self._destinations_n - 1` and `node1`
                                and `node2` are the same node
        :return: A dictionary containing the qubits and their fidelity
        """
        assert (1 <= node1 <= self._destinations_n - 1 and 1 <= node2 <= self._destinations_n - 1 and node1 != node2)

        self._perform_entanglement(node1, node2)
        return self._perform_entanglement_swapping(node1, node2)
        # return self._perform_fidelity_measurement(node1, node2)

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

        if channel_n == 0:
            source_name = "QuantumSource"
            remote_source_name = "RemoteQuantumSource"
        else:
            source_name = "QuantumSource" + str(channel_n)
            remote_source_name = "RemoteQuantumSource" + str(channel_n)

        # Initialize and start the protocols
        protocol_source: GenerateEntanglement = GenerateEntanglement(on_node=self._network.subcomponents["Source"],
                                                                     is_source=True, name="ProtocolSource",
                                                                     qsource_name=source_name)

        if node1 == self._destinations_n - 1 or node2 == self._destinations_n - 1:
            protocol_remote = GenerateEntanglement(on_node=self._network.subcomponents["RemoteNode"],
                                                   is_remote=True, name="ProtocolRemote",
                                                   qsource_name=remote_source_name)

            protocol_repeater = GenerateEntanglement(on_node=self._network.subcomponents["Repeater"],
                                                     is_repeater=True, name=f"ProtocolRepeater")

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

    def _perform_entanglement_swapping(self, node1: int,
                                       node2: int):  # TODO cognitive complexity is too high (sonarlint max is 15, this 16), reduce by extrapolating the logic to a helper function
        """
        Given two nodes, perform entanglement swapping only if either `node1` or `node2` is the Repeater.

        :param node1: The index of the first node
        :param node2: The index of the second node
        """
        try:
            if node1 == self._destinations_n - 1 or node2 == self._destinations_n - 1:
                m = self._network.subcomponents["Repeater"].qmemory.execute_instruction(INSTR_MEASURE_BELL,
                                                                                        output_key="M")
                # print(m)  # ({'M': [1]}, 0.0)
                state = m[0]["M"][0]
                # print(state)  # 1

                if state == 1:
                    # |01>
                    self._network.subcomponents["RemoteNode"].qmemory.execute_instruction(INSTR_X)
                elif state == 2:
                    # |11>
                    self._network.subcomponents["RemoteNode"].qmemory.execute_instruction(INSTR_Z)
                    self._network.subcomponents["RemoteNode"].qmemory.execute_instruction(INSTR_X)
                elif state == 3:
                    # |10>
                    self._network.subcomponents["RemoteNode"].qmemory.execute_instruction(INSTR_Z)
        except MemPositionEmptyError:
            pass

        try:
            node1_label = f"Node{node1}" if node1 != self._destinations_n - 1 else "RemoteNode"
            node2_label = f"Node{node2}" if node2 != self._destinations_n - 1 else "RemoteNode"

            qubit_node1, = self._network.subcomponents[node1_label].qmemory.pop(0)
            qubit_node2, = self._network.subcomponents[node2_label].qmemory.pop(0)
            _, = self._network.subcomponents["Repeater"].qmemory.peek(0)
            _, = self._network.subcomponents["Repeater"].qmemory.peek(1)
            entanglement_fidelity: float = qubits.fidelity([qubit_node1, qubit_node2], b00)

            if node1_label == "RemoteNode" or node2_label == "RemoteNode":
                try:
                    self._network.subcomponents["Repeater"].qmemory.discard(0)
                except:
                    pass

                try:
                    self._network.subcomponents["Repeater"].qmemory.discard(1)
                except:
                    pass

            result = {"qubits": (qubit_node1, qubit_node2), "fidelity": entanglement_fidelity, "error": False}
        except ValueError:
            result = {"message": "Either one or both Qubits were lost during transfer", "error": True}

        return result

    def _perform_new_entanglement_swapping(self, node1: int, node2: int, node3: int, debug: bool = False) \
            -> List[Dict[str, Union[List[Qubit], float, bool]]]:  # TODO cognitive complexity is too high (sonarlint max is 15, this 20), reduce by extrapolating the logic to a helper function
        """
        Given three nodes, perform entanglement swapping only if either `node1` or `node2` or `node3` is the Repeater.

        :param node1: The index of the first node
        :param node2: The index of the second node
        :param node3: The index of the third node
        :return: A dictionary containing the qubits and their fidelity
        """
        repeater_memory = self._network.subcomponents["Repeater"].qmemory
        remotenode_memory = self._network.subcomponents["RemoteNode"].qmemory
        try:
            if any(single_node == self._destinations_n - 1 for single_node in [node1, node2, node3]):
                m_mem_positions = [0, 1]
                m1_mem_positions = [2, 3]
                m = (repeater_memory.execute_instruction(INSTR_MEASURE_BELL, m_mem_positions, output_key="M"))
                m1 = (repeater_memory.execute_instruction(INSTR_MEASURE_BELL, m1_mem_positions, output_key="M"))
                state = m[0]["M"][0]
                state1 = m1[0]["M"][0]
                if debug:
                    print('_perform_new_entanglement_swapping: m= ', m, 'm1= ', m1)
                    print('Bell measurement in repeater: state', state, "state1", state1)

                # swap the qubits in memory position 0 and 1,
                # and then apply the necessary gates
                # then do the same for the position 2 and 3

                # create helper function to apply the gates, this replaces a chain of if-elif-else statements
                def apply_gates(curr_state: int, position: int) -> None:
                    """
                    Apply the necessary gates to the qubit in the memory position (in the RemoteNode),
                    based on the state (in the repeater).
                    :param curr_state: The state of the qubit in the Repeater memory position (0, 1, 2, or 3)
                    :param position: The memory position in the RemoteNode (0 or 1)
                    """
                    # dictionary with the instructions to apply based on the state of the qubit
                    # (represented w numbers, input of the function curr_state or as bell states in the comments)
                    instructions = {
                        0: [],  # |00> (no gates to apply) # TODO ask if this is correct
                        1: [INSTR_X],  # |01>
                        2: [INSTR_Z, INSTR_X],  # |11>
                        3: [INSTR_Z]  # |10>
                    }
                    # get the instructions based on the state of the qubit in the memory position
                    get_instructions = instructions[curr_state]
                    # apply the instructions to the qubit in the memory position (in the RemoteNode)
                    for instr in get_instructions:
                        remotenode_memory.execute_instruction(instr, [position])
                        #, output_key="M" , inplace=True, repetitions=1, position=position)  # position=position
                        if debug:
                            print(f"Applying instruction {instr} to the qubit "
                                  f"in memory position {position} in the RemoteNode")

                # apply gates for first and second state/position
                apply_gates(state, 0)
                apply_gates(state1, 1)
        except MemPositionEmptyError as e:
            print(e)

        try:
            labels = [f"Node{node_n}" if node_n != self._destinations_n - 1 else "RemoteNode"
                      for node_n in [node1, node2, node3, node3]]  # the last 2 are always "RemoteNode"
            mem_positions = [0, 0, 0, 1]  # 1 because "RemoteNode" has 2 mem positions
            # pop the qubits from the memory positions in the nodes specified by the labels (none repeater) & positions
            qubit_node1, qubit_node2, qubit_node3, qubit_node3_1 = \
                [self._network.subcomponents[label].qmemory.pop(mem_pos)[0]
                 for label, mem_pos in zip(labels, mem_positions)]
            # peak in all the repeater memory positions, from 0 to 3 (both included)
            for i in range(4):
                _, = repeater_memory.peek(i)

            def return_results(qubit1: Qubit, qubit2: Qubit, qubit3: Qubit, qubit4: Qubit) \
                    -> List[Dict[str, Union[List[Qubit], float, bool]]]:
                """
                Return the results of the entanglement swapping.

                :param qubit1: The first qubit
                :param qubit2: The second qubit
                :param qubit3: The third qubit
                :param qubit4: The fourth qubit
                :return: A dictionary containing the qubits and their fidelity
                """
                channel_1_pair = [qubit1, qubit4]
                channel_0_pair = [qubit2, qubit3]

                # measure fidelity between 2 pairs of qubits & return the results
                def calc_fidelity(pair1: List[Qubit], pair2: List[Qubit], reference_state: QRepr = b00) \
                        -> Tuple[float, float]:
                    """
                    Calculate the fidelity between two pairs of qubits.

                    :param pair1: The first pair of qubits
                    :param pair2: The second pair of qubits
                    :param reference_state: The reference state to compare the fidelity to
                    :return: The fidelity of the two pairs of qubits
                    """
                    return qubits.fidelity(pair1, reference_state), qubits.fidelity(pair2, reference_state)

                fidelity1, fidelity2 = calc_fidelity(channel_1_pair, channel_0_pair)
                result = {"qubits": channel_1_pair, "fidelity": fidelity1, "error": False}
                result1 = {"qubits": channel_0_pair, "fidelity": fidelity2, "error": False}
                return [result, result1]

            results = return_results(qubit_node1, qubit_node2, qubit_node3, qubit_node3_1)
            # try to discard the memory positions in the repeater
            if labels[-1] == "RemoteNode":  # same as node3_label: "RemoteNode"
                # list of the memory positions from 0 to 3 (both included)
                for i in range(4):
                    try:
                        repeater_memory.discard(i)
                    except:
                        pass
        except ValueError as e:
            print(e)
            results = {"message": "Some Qubits were lost during transfer", "error": True}
        return results

    def _perform_fidelity_measurement(self, node1: int, node2: int):
        """
        Given two nodes, measure the fidelity of their entangled qubits.

        :param node1: The index of the first node
        :param node2: The index of the second node
        :return: A dictionary containing the qubits and their fidelity
        """
        try:
            node1_label = f"Node{node1}" if node1 != self._destinations_n - 1 else "RemoteNode"
            node2_label = f"Node{node2}" if node2 != self._destinations_n - 1 else "RemoteNode"

            qubit_node1, = self._network.subcomponents[node1_label].qmemory.peek(0)
            qubit_node2, = self._network.subcomponents[node2_label].qmemory.peek(0)
            entanglement_fidelity: float = qubits.fidelity([qubit_node1, qubit_node2], b00)

            result = {"qubits": (qubit_node1, qubit_node2), "fidelity": entanglement_fidelity, "error": False}
        except ValueError:
            result = {"message": "Either one or both Qubits were lost during transfer", "error": True}

        return result
