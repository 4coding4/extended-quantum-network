from netsquid.nodes import Network


class MemorySnapshot:
    """
    A class to take a snapshot of the memories of the subcomponents of the network.
    :param network: The network to take the snapshot of.
    :param node1: The first node of the network.
    :param node2: The second node of the network.
    :param node4: The 4. node of the network equal to the remote node of the network.
    """

    def __init__(self, network: Network, node1: int, node2: int, node4: int):
        self._network = network
        self.node1 = node1
        self.node2 = node2
        assert node4 == 4  # The remote node must be the 4th node of the network.
        self.node4 = node4

    def memory_access(self, name, position):
        """
        Access the memory at the given position of the subcomponent.

        :param name: Name of the quantum memory
        :param position: Position in the memory
        :return qubit: The qubit at the given position or None if the memory is empty.
        :raises ValueError: If the position is out of range or if the memory is empty.
        :raises KeyError: If the memory does not exist.
        :raises IndexError: If the memory does not contain the given position.
        :raises AttributeError: If the memory does not have the peek method.
        :raises TypeError: If the memory does not contain qubits.
        :raises MemoryError: If the memory contains noise.
        :raises TimeoutError: If the memory does not respond in time.
        :raises Exception: If any other error occurs.
        :raises NotImplementedError: If the memory does not support the peek method.
        :raises RuntimeError: If the memory does not support the peek method.
        :raises AttributeError: If the memory does not support the peek method.
        :raises TypeError: If the memory does not support the peek method.
        """
        skip_noise = True
        el, = self._network.subcomponents[name].qmemory.peek(position, skip_noise)
        return el

    def multi_access(self, names_positions):
        """
        Access multiple memories at the given positions of the subcomponents.
        :param names_positions: List of tuples (name, position) for each memory to access.
        :return: A dictionary of memory names to the qubits at the given positions.
        """
        names, positions = names_positions
        return {f"{name}_m{pos}": self.memory_access(name, pos) for name, pos in zip(names, positions)}

    def repeater(self):
        """
        Returns the names and positions of the repeater's memories.
        :return: Tuple of lists of names and positions of the repeater's memories.
        """
        names = ["Repeater"] * 4  # TODO refactor, put the number of memories as a parameter and generate the lists accordingly
        positions = [0, 1, 2, 3]
        return names, positions

    def nodes(self):
        """
        Returns the names and positions of the nodes' memories.
        :return: Tuple of lists of names and positions of the nodes' memories.
        """
        names = [f"Node{self.node1}", f"Node{self.node2}"]  # TODO refactor, put the number of memories as a parameter and generate the lists accordingly
        positions = [0, 0]
        return names, positions

    def remote_node(self):
        """
        Returns the names and positions of the remote node's memories.
        :return: Tuple of lists of names and positions of the remote node's memories.
        """
        names = ["RemoteNode"] * 2  # TODO refactor, put the number of memories as a parameter and generate the lists accordingly
        positions = [0, 1]
        return names, positions

    def show_all_memory_positions(self, initial_msg="", end_msg="", line_width=80):
        """
        Observer in repeater to check if the q bits are there by peaking in all the memory positions
        """
        line = "-" * line_width

        if initial_msg != "":
            print(f"{line}\n" + initial_msg)

        # run the repeater, nodes and remote node, to get the tuples of names and positions of the memories
        names_positions = [self.repeater(), self.nodes(), self.remote_node()]
        # access the memories at the given positions (of the subcomponents) and
        # store the results in a list of dictionaries
        all_mem = [self.multi_access(names_positions) for names_positions in names_positions]
        # print the results in a formatted way for each memory position 1 pro line
        print("\n".join([f"{k}: {v}" for d in all_mem for k, v in d.items()]))

        if end_msg != "":
            print(end_msg + f"\n{line}")
