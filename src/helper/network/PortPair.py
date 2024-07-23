class PortPair:
    """
    Represents a pair of source and destination ports of a quantum channel.
    """
    _source: str = None
    _destination: str = None
    _name: str = None

    def __init__(self, source: str, destination: str, name: str = None):
        """
        The constructor of the PortPair class.

        :param source: The source port name
        :param destination: The destination port name
        :param name: The name of the port pair connection
        """
        self._source = source
        self._destination = destination
        self._name = name

    ###########
    # GETTERS #
    ###########

    @property
    def source(self) -> str:
        """
        :type: str
        """
        return self._source

    @property
    def destination(self) -> str:
        """
        :type: str
        """
        return self._destination

    @property
    def name(self) -> str:
        """
        :type: str
        """
        return self._name

    def get_all(self) -> tuple:
        """
        :type: tuple
        """
        return self._source, self._destination, self._name

    def show(self) -> str:
        """
        :type: str
        """
        return f"{self._source} -> {self._destination}, {self._name}"
