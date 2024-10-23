import os
import numpy as np
from app.filters.SvgFilterRenderer import SvgFilterRenderer

class ComponentsCalculator:
    def __init__(self):
        self.circuit = None
        self.r = []
        self.c = []
        self.k = []
        self.ra = []
        self.rb = []
        self.ga = None
        self.rout = None
        self.rx = None
        self.ry = None

    def calculate_low_pass_components(self, poles, c = 0.01e-6, ra = 1e4, rout = 1e4):
        self.rout = rout

        current_dir = os.path.dirname(os.path.abspath(__file__))
        svg_path = os.path.join(current_dir, "../static/img/output.svg")
        self.circuit = SvgFilterRenderer(filename=svg_path)

        for i, pole in enumerate(poles):
            if i == 0 and pole[0] == 0:
                self.r.append(1 / (pole[2] * c))
                self.c.append(c)

                self.circuit.add_low_pass_1(self.r[i], self.c[i])
            else:
                self.r.append(1 / np.sqrt(pole[2] * c**2))
                self.c.append(c)
                self.k.append(3 - (pole[1] / np.sqrt(pole[2])))
                self.ra.append(ra)
                self.rb.append(ra * (2 - (pole[1] / np.sqrt(pole[2]))))

                self.circuit.add_low_pass_2(self.r[i], self.c[i], self.ra[i - 1], self.rb[i - 1])

        self.ga = np.prod(self.k)
        self.rx = self.ga * rout
        self.ry = self.ga * (rout / (self.ga - 1))

        self.circuit.add_gain_adjustment(self.rx, self.ry)

        pass

    def save_circuit(self) -> None:
        self.circuit.save_dwg()

        pass