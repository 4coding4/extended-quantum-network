from netsquid.components.models import qerrormodels

class T1T2ErrorModel:
    """
    Commonly used phenomenological noise model based on T1 and T2 times.

    Parameters
    T1 (float):
        T1 time, dictating amplitude damping component.
    T2 (float):
        T2 time, dictating dephasing component.
        Note that this is what is called T2 Hahn, as opposed to free induction decay T2*
    """

    t1: float = 0.0000
    t2: float = 0.0001
    t1t2_noise_model: qerrormodels.T1T2NoiseModel = qerrormodels.T1T2NoiseModel(t1, t2)

