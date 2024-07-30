import unittest

from netsquid.components.component import ConstrainedMap

from src.helper.network.Factory.QuantumProcessor import QuantumProcessorFactory


class TestHelpersNetworkFactoryQuantumProcessor(unittest.TestCase):
    factory = QuantumProcessorFactory()

    def test_get(self):
        name = "name"
        pos = 2
        self.factory.get(name, pos)
        self.assertEqual(self.factory.get(name, pos).name, "name")
        self.assertEqual(self.factory.get(name, pos).properties, ConstrainedMap({'num_positions': 2}))



if __name__ == "__main__":
    unittest.main()
