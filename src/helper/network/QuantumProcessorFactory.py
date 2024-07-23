from netsquid.components import QuantumProcessor


class QuantumProcessorFactory:
    """
    Represents the quantum Processors.
    """

    @staticmethod
    def get_processor(name, mem_positions):
        """
        Get QuantumProcessor component with default settings.
        """
        return QuantumProcessor(name,
                                num_positions=mem_positions,
                                fallback_to_nonphysical=True
                                )
