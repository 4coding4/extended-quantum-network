from netsquid.components import QuantumProcessor


def get_processor(name, mem_positions):
    return QuantumProcessor(name,
                            num_positions=mem_positions,
                            fallback_to_nonphysical=True
                            )
