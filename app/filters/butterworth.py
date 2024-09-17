import numpy as np

def passa_baixas_normalizado(a_pass, a_stop, w_pass, w_stop):
    w_r = w_stop / w_pass
    e = np.sqrt(10**(-0.1 * a_pass) - 1)
    n = int(np.ceil(np.log10((10**(-0.1 * a_stop) - 1) / (10**(-0.1 * a_pass) - 1)) / (2 * np.log10(w_r))))
    r = e**(-1 / n)

    if n % 2 == 0:
        m = (n // 2) - 1
    else:
        m = ((n - 1) // 2) - 1

    z = []
    p = []
    k = []

    for i in range(m + 1):
        theta = (np.pi * (2 * i + n + 1)) / (2 * n)

        sigma = r * np.cos(theta)
        omega = r * np.sin(theta)

        z.append((0, 0, 0))
        p.append((1, -2 * sigma, sigma**2 + omega**2))
        k.append(sigma**2 + omega**2)

    if n % 2 != 0:
        z.insert(0, (0, 0, 0))
        p.insert(0, (0, 1, r))
        k.insert(0, r)

    return {
        'Omega_r': w_r,
        'epsilon': e,
        'ordem': n,
        'm': m,
        'R': r,
        'Hn': {
            'zeros': z,
            'polos': p,
            'ganho': k
        }
    }