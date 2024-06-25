from netsquid import b00
from netsquid.components import QSource, SourceStatus, FixedDelayModel
from netsquid.qubits import StateSampler


def get_source(name, delay, num_ports):
    return QSource(name,
                   state_sampler=StateSampler([b00]),
                   status=SourceStatus.EXTERNAL,
                   models={"emission_delay_model": FixedDelayModel(delay=delay)},
                   num_ports=num_ports
                   )
