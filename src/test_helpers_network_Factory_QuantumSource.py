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
        self.assertEqual(name,
                         self.factory.get(name).name)
        self.assertEqual(ConstrainedMap({'trigger_delay': 0.0}),
                         self.factory.get(name).properties)
        self.assertEqual(type(StateSampler([b00])),
                         type(self.factory.get(name).state_sampler))



# if __name__ == "__main__":
#     unittest.main()
