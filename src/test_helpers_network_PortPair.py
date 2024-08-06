import unittest

from src.helper.network.PortPair import PortPair


class TestHelpersNetworkPortPair(unittest.TestCase):
    pp: PortPair = PortPair("source", "destination", "name")

    def test_source(self):
        self.assertEqual("source",
                         self.pp.source)

    def test_destination(self):
        self.assertEqual("destination",
                         self.pp.destination)

    def test_name(self):
        self.assertEqual("name",
                         self.pp.name)

    def test_get_all(self):
        self.assertEqual(("source", "destination", "name"),
                         self.pp.get_all())

    def test_show(self):
        self.assertEqual("source -> destination, name",
                         self.pp.show())
