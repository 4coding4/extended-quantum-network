from netsquid.components import T1T2NoiseModel


class T1T2Error:
    """
    Commonly used phenomenological noise model based on T1 and T2 times.


    Model parameters
    ----------------
    t1:
        T1 time, dictating amplitude damping component.

    t2:
        T2 time, dictating dephasing component.
    """
    _t1: float = 0.0000
    _t2: float = 0.0001

    _noise_model: T1T2NoiseModel = None


    def __init__(self):
        self._noise_model = T1T2NoiseModel(self._t1, self._t2)

    ###########
    # GETTERS #
    ###########

    @property
    def t1(self) -> float:
        """
        :type: float
        """
        return self._t1

    @property
    def t2(self) -> float:
        """
        :type: float
        """
        return self._t2

    @property
    def noise_model(self) -> T1T2NoiseModel:
        """
        :type: T1T2NoiseModel
        """
        return self._noise_model
