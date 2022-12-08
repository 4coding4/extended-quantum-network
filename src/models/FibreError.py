from netsquid.components import FibreLossModel
from numpy.random import RandomState


class FibreError:
    """
    Model for exponential photon loss on fibre optic channels. Uses length of transmitting channel to sample an
    exponential loss probability.


    Model parameters
    ----------------
    p_loss_init:
        Initial probability of losing a photon once it enters a channel. e.g. due to frequency conversion.

    p_loss_length:
        Photon survival probability per channel length measured in dB/km.

    rng:
        Random number generator to use. If None then get_random_state of numpy is used. get_random_state uses Mersenne
        Twister pseudo-random number generator.
    """

    _p_loss_init: float = 0.2
    _p_loss_length: float = 0.25
    _rng: RandomState = None

    _loss_model: FibreLossModel = None


    def __init__(self):
        self._loss_model: FibreLossModel = FibreLossModel(self._p_loss_init, self._p_loss_length, self._rng)

    ###########
    # GETTERS #
    ###########

    @property
    def p_loss_init(self) -> float:
        """
        :type: float
        """
        return self._p_loss_init

    @property
    def p_loss_length(self) -> float:
        """
        :type: float
        """
        return self._p_loss_length

    @property
    def rng(self) -> RandomState:
        """
        :type: RandomState
        """
        return self._rng

    @property
    def loss_model(self) -> FibreLossModel:
        """
        :type: FibreLossModel
        """
        return self._loss_model
