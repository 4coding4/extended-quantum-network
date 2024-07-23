from netsquid.components import QuantumChannel


class QuantumChannelFactory:
    """
    Factory class for creating quantum channels.
    """

    def __init__(self, length, models):
        """
        Create a quantum channel factory.

        Parameters
        ----------
        length:
            (float) – Length of the channel [km].
        models:
            (dict) – Dictionary of models to use for the channel.
        """
        self.length = length
        self.models = models

    def get_channel(self, name):
        """
        Get a quantum channel with the given name.

        Parameters
        ----------
        name:
            (str) – Name of the channel.

        Returns
        -------
        QuantumChannel
            Quantum channel with the given name.
        """
        return QuantumChannel("Q" + name,
                              length=self.length,
                              models=self.models
                              )
