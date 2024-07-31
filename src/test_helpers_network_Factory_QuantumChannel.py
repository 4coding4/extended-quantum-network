import unittest

from netsquid.components.component import ConstrainedMap

from src.helper.network.Factory.QuantumChannel import QuantumChannelFactory


class TestHelpersNetworkFactoryQuantumChannel(unittest.TestCase):
    length, models = 1, {}
    factory = QuantumChannelFactory(length, models)

    def test_get(self):
        name = "name"
        self.assertEqual("Q" + name,
                         self.factory.get(name).name)
        self.assertEqual(ConstrainedMap({'length': 1}),
                         self.factory.get(name).properties)



# if __name__ == "__main__":
#     unittest.main()
