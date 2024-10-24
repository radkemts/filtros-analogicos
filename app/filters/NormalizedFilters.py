import numpy as np

class NormalizedFilters:
    def __init__(self):
        """
            Initializes the normalized filter parameters.

            Args:
        """

        self.a_pass = None
        self.a_stop = None
        self.w_r = None
        self.e = None
        self.approx = None
        self.n = None
        self.r = None
        self.d = None
        self.m = None
        self.theta = []
        self.phi = []
        self.sigma = []
        self.omega = []
        self.n_z = []
        self.n_p = []
        self.n_k = []

    def create_butterworth(self, a_pass: float|int, a_stop: float|int, w_r: float|int) -> 'NormalizedFilters':
        """
            Creates the normalized Butterworth low-pass filter parameters.

            Args:
                a_pass (float or int): Passband attenuation in dB.
                a_stop (float or int): Stopband attenuation in dB.
                w_r (float or int): Normalized angular frequency.

            Returns:
                NormalizedFilters: The current instance with updated filter parameters.
        """

        self.approx = 'butterworth'
        self.a_pass = a_pass
        self.a_stop = a_stop
        self.w_r = w_r
        self.e = np.sqrt(10**(-0.1 * a_pass) - 1)
        self.n = int(np.ceil(np.log10((10**(-0.1 * a_stop) - 1) / (10**(-0.1 * a_pass) - 1)) / (2 * np.log10(w_r))))
        self.r = self.e**(-1 / self.n)
        self.m = (self.n // 2) - 1 if self.n % 2 == 0 else ((self.n - 1) // 2) - 1

        for i in range(self.m + 1):
            self.theta.append((np.pi * (2 * i + self.n + 1)) / (2 * self.n))

            self.sigma.append(self.r * np.cos(self.theta[i]))
            self.omega.append(self.r * np.sin(self.theta[i]))

            self.n_z.append((0, 0, 0))
            self.n_p.append((1, -2 * self.sigma[i], self.sigma[i]**2 + self.omega[i]**2))
            self.n_k.append(self.sigma[i]**2 + self.omega[i]**2)

        if self.n % 2 != 0:
            self.n_z.insert(0, (0, 0, 0))
            self.n_p.insert(0, (0, 1, self.r))
            self.n_k.insert(0, self.r)

        return self

    def create_chebyshev(self, a_pass: float|int, a_stop: float|int, w_r: float|int) -> 'NormalizedFilters':
        """
            Creates the normalized Chebyshev low-pass filter parameters.

            Args:
                a_pass (float or int): Passband attenuation in dB.
                a_stop (float or int): Stopband attenuation in dB.
                w_r (float or int): Normalized angular frequency.

            Returns:
                NormalizedFilters: The current instance with updated filter parameters.
        """

        self.approx = 'chebyshev'
        self.a_pass = a_pass
        self.a_stop = a_stop
        self.w_r = w_r
        self.e = np.sqrt(10 ** (-0.1 * a_pass) - 1)
        self.n = int(np.ceil(np.acosh(np.sqrt((10 ** (-0.1 * a_stop) - 1) / (10 ** (-0.1 * a_pass) - 1))) / (np.acosh(w_r))))
        self.d = np.asinh(1 / self.e) / self.n
        self.m = (self.n // 2) - 1 if self.n % 2 == 0 else ((self.n - 1) // 2) - 1

        for i in range(self.m + 1):
            self.phi.append((np.pi * (2 * i + 1)) / (2 * self.n))

            self.sigma.append(-np.sinh(self.d) * np.sin(self.phi[i]))
            self.omega.append(np.cosh(self.d) * np.cos(self.phi[i]))

            self.n_z.append((0, 0, 0))
            self.n_p.append((1, -2 * self.sigma[i], self.sigma[i] ** 2 + self.omega[i] ** 2))
            self.n_k.append(self.sigma[i] ** 2 + self.omega[i] ** 2)

        if self.n % 2 != 0:
            self.n_z.insert(0, (0, 0, 0))
            self.n_p.insert(0, (0, 1, np.sinh(self.d)))
            self.n_k.insert(0, np.sinh(self.d))

        return self