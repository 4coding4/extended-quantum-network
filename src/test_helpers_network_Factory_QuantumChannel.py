import unittest

from netsquid.components.component import ConstrainedMap

from src.helper.network.Factory.QuantumChannel import QuantumChannelFactory


class TestHelpersNetworkFactoryQuantumChannel(unittest.TestCase):
    length, models = 1, {}
    factory = QuantumChannelFactory(length, models)

    def test_get(self):
        name = "name"
        self.factory.get(name)
        self.assertEqual(self.factory.get(name).name, "Qname")
        self.assertEqual(self.factory.get(name).properties, ConstrainedMap({'length': 1}))



if __name__ == "__main__":
    unittest.main()
