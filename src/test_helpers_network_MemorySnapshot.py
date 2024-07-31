import unittest

from src.helper.network.MemorySnapshot import MemorySnapshot
from src.network.StarNetwork import StarNetwork


class TestHelpersNetworkMemorySnapshot(unittest.TestCase):
    # test w default values in protocol a
    star_network = StarNetwork({})
    node1: int = 1
    node2: int = 2
    node3: int = 4
    debug: bool = True
    repeater_mem_positions: int = 4
    node_mem_positions: int = 1
    remote_node_mem_positions: int = 2
    memory_snapshot = MemorySnapshot(star_network.network, node1, node2, node3,
                                     repeater_mem_positions,
                                     node_mem_positions,
                                     remote_node_mem_positions)

    def test_show_all_memory_positions(self):
        msg = self.memory_snapshot.show_all_memory_positions()
        expected = ("--------------------------------------------------------------------------------\nRepeater_m0: "
                    "None\nRepeater_m1: None\nRepeater_m2: None\nRepeater_m3: None\nNode1_m0: None\nNode2_m0: "
                    "None\nRemoteNode_m0: None\nRemoteNode_m1: NoneIf it is working correctly, the output should have "
                    "\n--------------------------------------------------------------------------------")
        self.assertEqual(expected, msg)


if __name__ == "__main__":
    unittest.main()
