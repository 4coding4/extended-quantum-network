class PortPair:
    _source: str = None
    _destination: str = None


    def __init__(self, source: str, destination: str):
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
