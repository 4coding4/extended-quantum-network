from src.models.DynamicFibreDelay import DynamicFibreDelay
from src.models.FibreError import FibreError
from src.models.T1T2Error import T1T2Error


class Combined:
    """
    This class is used to combine the 3 models (with default parameters) in order to import them into the network
    directly.


    Instructions
    ------------
    1. Import this class into the network
        from src.models.Combined import Combined

    2. Connect the models to the network (in specific to the QuantumChannel).
        models = Combined.models
    """
    models: dict = dict(
        quantum_loss_model=FibreError.loss_model,
        quantum_noise_model=T1T2Error.noise_model,
        quantum_delay_model=DynamicFibreDelay.fibre_delay_model
    )
