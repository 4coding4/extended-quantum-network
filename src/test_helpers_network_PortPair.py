import unittest

from src.helper.network.PortPair import PortPair


class TestHelpersNetworkPortPair(unittest.TestCase):
    pp: PortPair = PortPair("source", "destination", "name")

    def test_source(self):
        self.assertEqual(self.pp.source, "source")

    def test_destination(self):
        self.assertEqual(self.pp.destination, "destination")

    def test_name(self):
        self.assertEqual(self.pp.name, "name")

    def test_get_all(self):
        self.assertEqual(self.pp.get_all(), ("source", "destination", "name"))

    def test_show(self):
        self.assertEqual(self.pp.show(), "source -> destination, name")


if __name__ == "__main__":
    unittest.main()
