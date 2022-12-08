from netsquid.components import FibreDelayModel


class DynamicFibreDelayModel:
    """
    Transmission delay model based on constant speed of photons through fibre. The travel distance is given by length
    of channel.

    Notes
    -----
    The default c refers to the speed of light in a f1 fibre cable, which is 200000 km/s, ~30% slower than the speed of
    light in a vacuum.

    Model parameters
    ----------------
    c:
        (float, optional) – Fixed speed of photons through the channel [km/s].
    """
    _c: float = 200000
    _fibre_delay_model: FibreDelayModel = None


    def __init__(self):
        self.fibre_delay_model: FibreDelayModel = FibreDelayModel(self._c)

    ###########
    # GETTERS #
    ###########

    @property
    def c(self) -> float:
        """
        :type: float
        """
        return self._c

    @property
    def noise_model(self) -> FibreDelayModel:
        """
        :type: FibreDelayModel
        """
        return self._fibre_delay_model
