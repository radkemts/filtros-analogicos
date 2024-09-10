import numpy as np

from app.filters.butterworth import normalized_low_pass as nlpb
from app.filters.chebyshev import low_pass as lpc

def calcula(request):
    approx = request.form.get('approx', type=str)
    a_pass = request.form.get('a-pass', type=float)
    a_stop = request.form.get('a-stop', type=float)
    f_pass1 = request.form.get('f-pass1', type=float)
    f_stop1 = request.form.get('f-stop1', type=float)
    f_pass2 = request.form.get('f-pass2', type=float)
    f_stop2 = request.form.get('f-stop2', type=float)
    unidade = request.form.get('unidade', type=str)

    w_pass1 = 2 * np.pi * f_pass1
    w_stop1 = 2 * np.pi * f_stop1

    if f_pass2 is not None and f_stop2 is not None:
        w_pass2 = 2 * np.pi * f_pass2
        w_stop2 = 2 * np.pi * f_stop2
    else:
        w_pass2 = None
        w_stop2 = None

    match approx:
        case 'butterworth':
            resultado = nlpb(a_pass, a_stop, w_pass1, w_stop1)
        case 'chebyshev':
            resultado = lpc(a_pass, a_stop, w_pass1, w_stop1)
        case _:
            resultado = []

    resultado.update({
        'approx': approx,
        'a_pass': a_pass,
        'a_stop': a_stop,
        'f_pass1': f_pass1,
        'f_stop1': f_stop1,
        'f_pass2': f_pass2,
        'f_stop2': f_stop2,
        'w_pass1': w_pass1,
        'w_stop1': w_stop1,
        'w_pass2': w_pass2,
        'w_stop2': w_stop2,
        'unidade': unidade
    })

    return resultado