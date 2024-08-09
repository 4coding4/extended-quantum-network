import unittest

from netsquid.components import QSource
from netsquid.nodes import Node

from src.protocols.GenerateEntanglement import GenerateEntanglement


class TestProtocolsGenerateEntanglement(unittest.TestCase):

    # other methods are already tested/covered
    def test_is_connected(self):
        # create a node with nothing/no subcomponents
        node_name0 = "node"
        node0 = Node(node_name0)

        # create a node with a QSource subcomponent
        node_name = "node_w_source"
        node = Node(node_name)
        # create a source
        source_name = "test_source"
        source = QSource(source_name)
        # add the source to the node as a subcomponent
        node.subcomponents[source_name] = source

        # create protocols with the 2 nodes
        # node with no source
        p = GenerateEntanglement(node0, node_name, is_source=True)
        p1 = GenerateEntanglement(node0, node_name, is_source=True, qsource_name=source_name)
        # node with source
        ps = GenerateEntanglement(node, node_name, is_source=True)
        ps1 = GenerateEntanglement(node, node_name, is_source=True, qsource_name=source_name)

        # test is_connected
        self.assertFalse(p.is_connected)
        self.assertFalse(p1.is_connected)

        self.assertTrue(ps.is_connected)
        self.assertTrue(ps1.is_connected)


