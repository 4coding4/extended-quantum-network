import unittest

from netsquid.nodes import Network

from src.network.StarNetwork import StarNetwork


class TestNetworkStarNetwork(unittest.TestCase):
    star_network = StarNetwork()

    def test_star_network_setters_getters(self):
        self.assertEqual(Network, type(self.star_network.network))

        old_source_delay = self.star_network.source_delay
        self.assertEqual(1e5, old_source_delay)
        self.star_network.source_delay = 1e6
        self.assertEqual(1e6, self.star_network.source_delay)

        old_destinations_n = self.star_network.destinations_n
        self.assertEqual(5, old_destinations_n)
        self.star_network.destinations_n = 10
        self.assertEqual(10, self.star_network.destinations_n)

        old_channels_length = self.star_network.channels_length
        self.assertEqual(1, old_channels_length)
        self.star_network.channels_length = 2
        self.assertEqual(2 / 1000, self.star_network.channels_length)

        old_models = self.star_network.models
        self.assertIsNone(old_models)
        self.star_network.models = {}
        self.assertEqual({}, self.star_network.models)

        self.assertEqual(4, self.star_network.repeater_mem_positions)

        self.assertEqual(1, self.star_network.node_mem_positions)

        self.assertEqual(2, self.star_network.remote_node_mem_positions)
