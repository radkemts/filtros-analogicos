from app.filters.butterworth import passa_baixas_normalizado as butterworth

def passa_baixas_desnormalizado(a_pass, a_stop, w_pass, w_stop, aproximacao):
    w_0 = w_pass

    match aproximacao:
        case 'butterworth':
            resultado = butterworth(a_pass, a_stop, w_pass, w_stop)
        case _:
            resultado = {}

    zeros = resultado['Hn']['zeros']
    polos = resultado['Hn']['polos']
    ganho = resultado['Hn']['ganho']

    z = []
    p = []
    k = []

    for i, polo in enumerate(polos):
        if i == 0 and polo[0] == 0:
            z.append((0, zeros[i][1], zeros[i][2] * w_0))
            p.append((0, polo[1], polo[2] * w_0))
            k.append(ganho[i] * w_0)
        else:
            z.append((zeros[i][0], zeros[i][1] * w_0, zeros[i][2] * w_0**2))
            p.append((polo[0], polo[1] * w_0, polo[2] * w_0**2))
            k.append(ganho[i] * w_0**2)

    resultado.update({
        'w_0': w_0,
        'H': {
            'zeros': z,
            'polos': p,
            'ganho': k
        }
    })

    return resultado