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
    _p_loss_init: float = 0.09
    _p_loss_length: float = 0.25
    _rng: RandomState = None

    loss_model: FibreLossModel = FibreLossModel(_p_loss_init, _p_loss_length, _rng)
