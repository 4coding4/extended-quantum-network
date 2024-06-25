from netsquid.components import QuantumProcessor
from netsquid import b00
from netsquid.components import QSource, SourceStatus, FixedDelayModel
from netsquid.qubits import StateSampler


class QuantumComponents:
    @staticmethod
    def get_processor(name, mem_positions):
        return QuantumProcessor(name,
                                num_positions=mem_positions,
                                fallback_to_nonphysical=True
                                )

    @staticmethod
    def get_source(name, delay, num_ports):
        return QSource(name,
                       state_sampler=StateSampler([b00]),
                       status=SourceStatus.EXTERNAL,
                       models={"emission_delay_model": FixedDelayModel(delay=delay)},
                       num_ports=num_ports
                       )
