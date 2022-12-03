from netsquid.components.models import qerrormodels
from numpy.random import RandomState


class FibreErrorModel:
    """
    Model for exponential photon loss on fibre optic channels.

    Uses length of transmitting channel to sample an exponential loss probability.

    Parameters
    p_loss_init (float, optional):
        Initial probability of losing a photon once it enters a channel. e.g. due to frequency conversion.

    p_loss_length (float, optional):
        Photon survival probability per channel length [dB/km].

    rng (RandomState or None, optional):
        Random number generator to use. If None then get_random_state of numpy is used.
        get_random_state uses Mersenne Twister pseudo-random number generator.
    """

    p_loss_init: float = 0.2
    p_loss_length: float = 0.25
    rng: RandomState = None

    fibre_loss_model: qerrormodels.FibreLossModel = qerrormodels.FibreLossModel(p_loss_init, p_loss_length, rng)
