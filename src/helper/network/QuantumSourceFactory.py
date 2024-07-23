from netsquid import b00
from netsquid.components import QSource, SourceStatus, FixedDelayModel
from netsquid.qubits import StateSampler


class QuantumSourceFactory:
    """
    Factory class for creating quantum sources.
    """

    def __init__(self, delay, num_ports):
        """
        Create a quantum source factory.

        Parameters
        ----------
        delay:
            (float) – Delay of the source [ns].
        num_ports:
            (int) – Number of ports of the source.
        """
        self.delay = delay
        self.num_ports = num_ports

    def get_source(self, name):
        """
        Get a quantum source with the given name.

        Parameters
        ----------
        name:
            (str) – Name of the source.

        Returns
        -------
        QuantumSource
            Quantum source with the given name.
        """
        return QSource(name,
                       state_sampler=StateSampler([b00]),
                       status=SourceStatus.EXTERNAL,
                       models={"emission_delay_model": FixedDelayModel(delay=delay)},
                       num_ports=self.num_ports
                       )
