import os

import numpy as np
import svgwrite

def passa_baixas_sallen_key(zeros, polos, ganho):
    r_a = 1e4
    r_out = 1e4
    c = 10e-9

    r = []
    k = []
    r_b = []

    for i, polo in enumerate(polos):
        if i == 0 and polo[0] == 0:
            r.append(1 / (polo[2] * c))
            k.append(1)
        else:
            r.append(1 / np.sqrt(polo[2] * c**2))
            k.append(3 - (polo[1] / np.sqrt(polo[2])))
            r_b.append(r_a * (2 - (polo[1] / np.sqrt(polo[2]))))

    ga = np.prod(k)

    componentes = {
        'RA': r_a,
        'C': c,
        'R': r,
        'K': k,
        'RB': r_b,
        'Rx': ga * r_out,
        'Ry': ga * (r_out / (ga - 1))
    }

    return componentes

def passa_baixas_sallen_key_svg(x, y, r, c):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(current_dir, '../static/img/')
    filename = 'filtro.svg'
    path = os.path.join(directory, filename)

    dwg = svgwrite.Drawing(path, profile='tiny', size=(x + 335, y + 137))

    dwg.add(dwg.polygon(
        points=[
            (319.256 + x, 10.623 + y),
            (364.256 + x, 100.623 + y),
            (274.256 + x, 100.623 + y),
        ],
        fill='none',
        stroke='black',
        stroke_width=2,
        stroke_linejoin='round',
        transform=f'rotate(90, {x + 274.256}, {y + 10.623})'
    ))

    # Adiciona textos
    dwg.add(dwg.text(
        '+',
        insert=(186.256 + x, 43.865 + y),
        fill='black',
        font_size=26,
        font_family='Arial, sans-serif'
    ))
    dwg.add(dwg.text(
        '-',
        insert=(188.256 + x, 83.865 + y),
        fill='black',
        font_size=26,
        font_family='Arial, sans-serif'
    ))

    # Desenha a polyline
    dwg.add(dwg.polyline(
        points=[
            (44.256 + x, 35.623 + y),
            (64.256 + x, 35.623 + y),
            (69.256 + x, 45.623 + y),
            (74.256 + x, 25.623 + y),
            (79.256 + x, 45.623 + y),
            (84.256 + x, 25.623 + y),
            (89.256 + x, 45.623 + y),
            (94.256 + x, 25.623 + y),
            (99.256 + x, 35.623 + y),
            (184.256 + x, 35.623 + y),
        ],
        fill='none',
        stroke='black',
        stroke_width=2,
        stroke_linecap='round',
        stroke_linejoin='round'
    ))

    # Desenha linhas
    dwg.add(dwg.line(
        start=(144.256 + x, 75.623 + y),
        end=(114.256 + x, 75.623 + y),
        stroke='black',
        stroke_width=2
    ))
    dwg.add(dwg.line(
        start=(129.256 + x, 35.623 + y),
        end=(129.256 + x, 75.623 + y),
        stroke='black',
        stroke_width=2,
        stroke_linecap='round'
    ))
    dwg.add(dwg.line(
        start=(129.256 + x, 125.623 + y),
        end=(129.256 + x, 85.623 + y),
        stroke='black',
        stroke_width=2,
        stroke_linecap='round'
    ))
    dwg.add(dwg.line(
        start=(114.256 + x, 85.623 + y),
        end=(144.256 + x, 85.623 + y),
        stroke='black',
        stroke_width=2
    ))

    # Desenha a segunda polyline
    dwg.add(dwg.polyline(
        points=[
            (184.256 + x, 75.623 + y),
            (159.256 + x, 75.623 + y),
            (159.256 + x, 125.623 + y),
            (304.256 + x, 125.623 + y),
            (304.256 + x, 55.623 + y),
        ],
        fill='none',
        stroke='black',
        stroke_width=2,
        stroke_linecap='round',
        stroke_linejoin='round'
    ))

    # Desenha linha adicional
    dwg.add(dwg.line(
        start=(274.256 + x, 55.623 + y),
        end=(334.256 + x, 55.623 + y),
        stroke='black',
        stroke_width=2,
        stroke_linecap='round'
    ))

    # Adiciona textos adicionais
    dwg.add(dwg.text(
        r,
        insert=(79.942 + x, 17.794 + y),
        fill='black',
        font_size=20,
        font_family='Arial, sans-serif',
        text_anchor='middle'
    ))
    dwg.add(dwg.text(
        c,
        insert=(110.502 + x, 87.794 + y),
        fill='black',
        font_size=20,
        font_family='Arial, sans-serif',
        text_anchor='end'
    ))

    # Desenha o círculo
    dwg.add(dwg.circle(
        center=(38.256 + x, 35.623 + y),
        r=5,
        fill='none',
        stroke='black',
        stroke_width=2
    ))

    # Adiciona texto ao lado do círculo
    dwg.add(dwg.text(
        'Vin',
        insert=(29.237 + x, 40.867 + y),
        fill='black',
        font_size=20,
        font_family='Arial, sans-serif',
        text_anchor='end'
    ))

    dwg.add(dwg.polygon(
        points=[
            (149 + x, 136 + y),
            (159 + x, 146 + y),
            (139 + x, 146 + y)
        ],
        fill='none',
        stroke='black',
        stroke_width=2,
        stroke_linejoin='round',
        transform=f'rotate(180, {x + 139}, {y + 136})'
    ))

    dwg.save()

    return path