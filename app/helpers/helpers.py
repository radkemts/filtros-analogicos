def formato_engenharia(valor):
    prefixos = {
        -9: 'n',
        -6: 'u',
        -3: 'm',
        0: '',
        3: 'k',
        6: 'M',
    }

    if valor == 0:
        return '0'

    exponente = int('{:.0e}'.format(valor).split('e')[1])
    exponente = (exponente // 3) * 3

    valor_escala = valor / (10 ** exponente)

    prefixo = prefixos.get(exponente, f'e{exponente}')

    if valor_escala.is_integer():
        return f'{int(valor_escala)}{prefixo}'
    else:
        return f'{valor_escala:.2f}{prefixo}'
