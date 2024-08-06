import unittest

from netsquid.nodes import Network

from src.helper.network.Factory.QuantumProcessor import QuantumProcessorFactory
from src.helper.network.MemorySnapshot import MemorySnapshot


class TestHelpersNetworkMemorySnapshot(unittest.TestCase):
    def test_show_all_memory_positions(self):
        # test w default values in protocol a
        node1: int = 1
        node2: int = 2
        node3: int = 4
        repeater_mem_positions: int = 4
        node_mem_positions: int = 1
        remote_node_mem_positions: int = 2

        # create a network
        network = Network("Network")
        # add nodes to the network
        network.add_node("Node1")
        network.add_node("Node2")
        network.add_node("Repeater")
        network.add_node("RemoteNode")
        # subcomponents processor w memories
        quantum_processor_factory = QuantumProcessorFactory()
        network.nodes["Repeater"].add_subcomponent(
            quantum_processor_factory.get("QP_Repeater", repeater_mem_positions)
        )
        network.nodes["RemoteNode"].add_subcomponent(
            quantum_processor_factory.get("QP_RemoteNode", remote_node_mem_positions)
        )
        network.nodes["Node1"].add_subcomponent(
            quantum_processor_factory.get("QP_Node1", node_mem_positions)
        )
        network.nodes["Node2"].add_subcomponent(
            quantum_processor_factory.get("QP_Node2", node_mem_positions)
        )

        memory_snapshot = MemorySnapshot(network, node1, node2, node3,
                                         repeater_mem_positions,
                                         node_mem_positions,
                                         remote_node_mem_positions)
        msg = memory_snapshot.show_all_memory_positions(initial_msg=" ", end_msg=" ", line_width=0)
        expected = ("\n Repeater_m0: "
                    "None\nRepeater_m1: None\nRepeater_m2: None\nRepeater_m3: None\nNode1_m0: None\nNode2_m0: "
                    "None\nRemoteNode_m0: None\nRemoteNode_m1: NoneIf it is working correctly, the output should have "
                    " \n")
        self.assertEqual(expected, msg)


# if __name__ == "__main__":
#     unittest.main()
