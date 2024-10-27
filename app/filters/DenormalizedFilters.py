import numpy as np
from app.filters.NormalizedFilters import NormalizedFilters

class DenormalizedFilters(NormalizedFilters):
    def __init__(self):
        super().__init__()

        self.a_pass = None
        self.a_stop = None
        self.f_pass1 = None
        self.f_pass2 = None
        self.f_stop1 = None
        self.f_stop2 = None
        self.w_pass1 = None
        self.w_pass2 = None
        self.w_stop1 = None
        self.w_stop2 = None
        self.w_r = None
        self.w_0 = None
        self.d_z = []
        self.d_p = []
        self.d_k = []

    def _denormalize_low_pass(self, zeros, poles, gain) -> None:
        """
            Denormalizes the low-pass filter parameters.

            Args:
                zeros (list of tuples): Each tuple contains three float values representing zeros.
                poles (list of tuples): Each tuple contains three float values representing poles.
                gain (list of float or int): List of float or int values representing gain.

            Returns:
                None: This function modifies the instance attributes directly.
        """

        for i, pole in enumerate(poles):
            if i == 0 and pole[0] == 0:
                self.d_z.append((0, zeros[i][1], zeros[i][2] * self.w_0))
                self.d_p.append((0, pole[1], pole[2] * self.w_0))
                self.d_k.append(gain[i] * self.w_0)
            else:
                self.d_z.append((zeros[i][0], zeros[i][1] * self.w_0, zeros[i][2] * self.w_0 ** 2))
                self.d_p.append((pole[0], pole[1] * self.w_0, pole[2] * self.w_0 ** 2))
                self.d_k.append(gain[i] * self.w_0 ** 2)

            pass

    def create_low_pass_butterworth(self, a_pass: float|int, a_stop: float|int, f_pass: float|int, f_stop: float|int) -> 'DenormalizedFilters':
        self.a_pass = a_pass
        self.a_stop = a_stop
        self.f_pass1 = f_pass
        self.f_stop1 = f_stop
        self.w_pass1 = 2 * np.pi * f_pass
        self.w_stop1 = 2 * np.pi * f_stop
        self.w_r = self.w_stop1 / self.w_pass1
        self.w_0 = self.w_pass1

        handle = super().create_butterworth(self.a_pass, self.a_stop, self.w_r)

        self._denormalize_low_pass(handle.n_z, handle.n_p, handle.n_k)

        return self

    def create_low_pass_chebyshev(self, a_pass: float|int, a_stop: float|int, f_pass: float|int, f_stop: float|int) -> 'DenormalizedFilters':
        self.a_pass = a_pass
        self.a_stop = a_stop
        self.f_pass1 = f_pass
        self.f_stop1 = f_stop
        self.w_pass1 = 2 * np.pi * f_pass
        self.w_stop1 = 2 * np.pi * f_stop
        self.w_r = self.w_stop1 / self.w_pass1
        self.w_0 = self.w_pass1

        handle = super().create_chebyshev(self.a_pass, self.a_stop, self.w_r)

        self._denormalize_low_pass(handle.n_z, handle.n_p, handle.n_k)

        return self