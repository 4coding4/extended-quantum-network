from netsquid.components.component import Qubit
from netsquid.nodes import Network
from typing import List, Tuple


class MemorySnapshot:
    """
    A class to take a snapshot of the memories of the subcomponents of the network.
    :param network: The network to take the snapshot of.
    :param node1: The first node of the network.
    :param node2: The second node of the network.
    :param node4: The 4. node of the network equal to the remote node of the network.
    :param repeater_mem_positions: The number of memory positions in the repeater.
    :param node_mem_positions: The number of memory positions in each node.
    :param remote_node_mem_positions: The number of memory positions in the remote node.
    """

    def __init__(self, network: Network, node1: int, node2: int, node4: int,
                 repeater_mem_positions: int, node_mem_positions: int, remote_node_mem_positions: int):
        self._network = network
        self.node1 = node1
        self.node2 = node2
        assert node4 == 4  # The remote node must be the 4th node of the network.
        self.repeater_mem_positions = repeater_mem_positions
        self.node_mem_positions = node_mem_positions
        self.remote_node_mem_positions = remote_node_mem_positions

    def memory_access(self, name: str, position: int) -> Qubit:
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

    def multi_access(self, names_positions: Tuple[List[str], List[int]]) -> dict:
        """
        Access multiple memories at the given positions of the subcomponents.
        :param names_positions: List of tuples (name, position) for each memory to access.
        :return: A dictionary of memory names to the qubits at the given positions.
        """
        names, positions = names_positions
        return {f"{name}_m{pos}": self.memory_access(name, pos) for name, pos in zip(names, positions)}

    def repeater(self) -> Tuple[List[str], List[int]]:
        """
        Returns the names and positions of the repeater's memories.
        :return: Tuple of lists of names and positions of the repeater's memories.
        """
        names = ["Repeater"] * self.repeater_mem_positions  # TODO refactor, put the number of memories as a parameter and generate the lists accordingly
        # positions = [0, 1, 2, 3] # 0 to repeater_mem_positions-1
        positions = list(range(self.repeater_mem_positions))
        return names, positions

    def nodes(self) -> Tuple[List[str], List[int]]:
        """
        Returns the names and positions of the nodes' memories.
        :return: Tuple of lists of names and positions of the nodes' memories.
        """
        names = [f"Node{self.node1}", f"Node{self.node2}"]  # TODO refactor, put the number of memories as a parameter and generate the lists accordingly
        # positions = [0, 0] # 0 to node_mem_positions-1 *2 for two nodes
        positions = list(range(self.node_mem_positions)) * 2
        return names, positions

    def remote_node(self) -> Tuple[List[str], List[int]]:
        """
        Returns the names and positions of the remote node's memories.
        :return: Tuple of lists of names and positions of the remote node's memories.
        """
        names = ["RemoteNode"] * self.remote_node_mem_positions  # TODO refactor, put the number of memories as a parameter and generate the lists accordingly
        # positions = [0, 1] # 0 to remote_node_mem_positions-1
        positions = list(range(self.remote_node_mem_positions))
        return names, positions

    def show_all_memory_positions(self, initial_msg: str = "", end_msg: str = "", line_width: int = 80) -> str:
        """
        Observer in repeater to check if the q bits are there by peaking in all the memory positions
        :param initial_msg: The initial message to print.
        :param end_msg: The end message to print.
        :param line_width: The width of the line to print.
        :return: A string with the initial message, the memory positions and the end message.
        """
        line = "-" * line_width

        start_str = f"{line}\n" + initial_msg
        if initial_msg != "":
            print(start_str)

        # run the repeater, nodes and remote node, to get the tuples of names and positions of the memories
        names_positions = [self.repeater(), self.nodes(), self.remote_node()]
        # access the memories at the given positions (of the subcomponents) and
        # store the results in a list of dictionaries
        all_mem = [self.multi_access(names_positions) for names_positions in names_positions]
        # print the results in a formatted way for each memory position 1 pro line
        mid_str = "\n".join([f"{k}: {v}" for d in all_mem for k, v in d.items()])
        print(mid_str)

        end_str = "If it is working correctly, the output should have " + end_msg + f"\n{line}"
        if end_msg != "":
            print(end_str)

        return start_str + mid_str + end_str
