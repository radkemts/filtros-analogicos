import numpy as np

def normalized_low_pass(a_pass, a_stop, w_pass, w_stop):
    w_r = w_stop / w_pass
    e = np.sqrt(10**(-0.1 * a_pass) - 1)
    n = int(np.ceil(np.acosh(np.sqrt((10**(-0.1 * a_stop) - 1) / (10**(-0.1 * a_pass) - 1))) / (np.acosh(w_r))))
    d = np.asinh(1 / e) / n

    if n % 2 == 0:
        m = (n // 2) - 1
    else:
        m = ((n - 1) // 2) - 1

    z = []
    p = []
    k = []

    for i in range(m + 1):
        phi = (np.pi * (2 * i + 1)) / (2 * n)

        sigma = -np.sinh(d) * np.sin(phi)
        omega = np.cosh(d) * np.cos(phi)

        p.append((1, -2 * sigma, sigma**2 + omega**2))
        k.append(sigma**2 + omega**2)

    if n % 2 != 0:
        k.insert(0, np.sinh(d))
        p.insert(0, (0, 1, np.sinh(d)))

    return {
        'Omega_r': w_r,
        'epsilon': e,
        'ordem': n,
        'm': m,
        'D': d,
        'Hn': {
            'zeros': z,
            'polos': p,
            'ganho': k
        }
    }