import numpy as np

from app.filters.passa_baixas_desnormalizado import passa_baixas_desnormalizado
from app.filters.passa_baixas_sallen_key import passa_baixas_sallen_key, passa_baixas_sallen_key_svg
from app.helpers.helpers import formato_engenharia


def filtro(request):
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

        if f_pass1 > f_stop1 and f_stop2 < f_pass2:
            filtro = 'passa-banda'
        else:
            filtro = 'rejeita-banda'
    else:
        w_pass2 = None
        w_stop2 = None

        if f_pass1 < f_stop1:
            filtro = 'passa-baixas'
        else:
            filtro = 'passa-altas'

    if approx == 'butterworth':
        if filtro == 'passa-baixas':
            pb_desnormalizado = passa_baixas_desnormalizado(a_pass, a_stop, w_pass1, w_stop1, approx)
            componentes = passa_baixas_sallen_key(pb_desnormalizado['H']['zeros'], pb_desnormalizado['H']['polos'], pb_desnormalizado['H']['ganho'])
            passa_baixas_sallen_key_svg(0, 0, formato_engenharia(componentes['R'][0]), formato_engenharia(componentes['C']))
        else:
            pb_desnormalizado = {}
    elif approx == 'chebyshev':
        if filtro == 'passa-baixas':
            pb_desnormalizado = {}
        else:
            pb_desnormalizado = {}
    else:
        pb_desnormalizado = {}

    pb_desnormalizado.update({
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
        'unidade': unidade,
        'filtro': filtro
    })

    return pb_desnormalizado