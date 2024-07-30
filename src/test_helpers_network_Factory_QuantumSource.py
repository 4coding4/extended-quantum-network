import unittest

from netsquid.components.component import ConstrainedMap

from src.helper.network.Factory.QuantumSource import QuantumSourceFactory


class TestHelpersNetworkFactoryQuantumSource(unittest.TestCase):
    delay, num_ports = 1, 1
    factory = QuantumSourceFactory(delay, num_ports)

    def test_get(self):
        name = "name"
        self.factory.get(name)
        self.assertEqual(self.factory.get(name).name, "name")
        self.assertEqual(self.factory.get(name).properties, ConstrainedMap({'trigger_delay': 0.0}))



if __name__ == "__main__":
    unittest.main()
