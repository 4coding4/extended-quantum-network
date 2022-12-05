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
    # Documentation used in order to decide on the parameters for the T1T2ErrorModel
    # https://www.semanticscholar.org/paper/Phenomenological-noise-model-for-superconducting-Zhou-Joynt/25d147a437877e921828556def1f0b0375655291
    # https://arxiv.org/pdf/1102.5766.pdf
    # 1000 to 5000μB, μ=10^-6
    # https://arxiv.org/pdf/1102.3445.pdf
    # 10^-8, 10^-7 f
    # https://www.researchgate.net/profile/Florian-Dolde/publication/45934292_Dynamical_Decoupling_of_a_single_electron_spin_at_room_temperature/links/00b49529336f366f0d000000/Dynamical-Decoupling-of-a-single-electron-spin-at-room-temperature.pdf
    # https://www.researchgate.net/figure/Hahn-echo-decay-inset-T2-039-016-ms-CPMG-red-markers-T-CPMG-2-244_fig1_45934292
    # T2 = 0.39 ± 0.16 ms, T1ρ = 2.47 ± 0.27 ms, T1 = 5.93 ± 0.7 ms
    # https://forest-benchmarking.readthedocs.io/en/latest/examples/qubit_spectroscopy_t2.html
    # many values
    # https://www.nature.com/articles/s41534-019-0168-5
    # T1 = 49 μs and T2* = 95 μs
    # https://quantumcomputing.stackexchange.com/questions/26325/qubit-dephasing-times
    # T2* < T2 echo (not everybody agrees)
    # https://qiskit.org/documentation/experiments/tutorials/t2hahn_characterization.html <- T2 Hahn (lib qiskit and plot T2 Hahn experiments)

    t1: float = 49 * 10 ** -6
    # magic number, cannot exceed 100
    constant: float = 93.877
    # t2: float = (49/100) * 10 ** -6
    t2: float = (95 / (100 + constant)) * 10 ** -6
    t1t2_noise_model: qerrormodels.T1T2NoiseModel = qerrormodels.T1T2NoiseModel(t1, t2)
