import unittest

from netsquid import b00
from netsquid.components.component import ConstrainedMap
from netsquid.qubits import StateSampler

from src.helper.network.Factory.QuantumSource import QuantumSourceFactory


class TestHelpersNetworkFactoryQuantumSource(unittest.TestCase):
    delay, num_ports = 1, 1
    factory = QuantumSourceFactory(delay, num_ports)

    def test_get(self):
        name = "name"
        self.factory.get(name)
        self.assertEqual(self.factory.get(name).name, "name")
        self.assertEqual(self.factory.get(name).properties, ConstrainedMap({'trigger_delay': 0.0}))
        self.assertEqual(type(self.factory.get(name).state_sampler), type(StateSampler([b00])))



if __name__ == "__main__":
    unittest.main()
