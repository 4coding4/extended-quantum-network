import unittest

from netsquid.components.component import ConstrainedMap

from src.helper.network.Factory.QuantumProcessor import QuantumProcessorFactory


class TestHelpersNetworkFactoryQuantumProcessor(unittest.TestCase):
    factory = QuantumProcessorFactory()

    def test_get(self):
        name = "name"
        pos = 2
        self.assertEqual(name,
                         self.factory.get(name, pos).name)
        self.assertEqual(ConstrainedMap({'num_positions': 2}),
                         self.factory.get(name, pos).properties)
