class PortPair:
    """
    Represents a pair of source and destination ports of a quantum channel.
    """
    _source: str = None
    _destination: str = None


    def __init__(self, source: str, destination: str):
        """
        The constructor of the PortPair class.

        :param source: The source port name
        :param destination: The destination port name
        """
        self._source = source
        self._destination = destination

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
