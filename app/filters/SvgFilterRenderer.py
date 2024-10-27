import math
import svgwrite

def eng_format(value: float | int) -> str:
    """
    Formats a numerical value into engineering notation with appropriate SI prefixes.
    """
    prefixes = {
        -12: 'p',
        -9: 'n',
        -6: 'μ',
        -3: 'm',
        0: '',
        3: 'k',
        6: 'M',
        9: 'G',
        12: 'T'
    }

    sign = '-' if value < 0 else ''
    value = abs(value)

    if value == 0:
        return '0'

    exponent = int(math.floor(math.log10(value)))
    exponent = exponent - (exponent % 3)
    scaled_value = value / (10 ** exponent)

    if abs(scaled_value - round(scaled_value)) < 10e-12:
        scaled_value = round(scaled_value)

    scaled_value = float(scaled_value)

    if exponent in prefixes:
        if scaled_value.is_integer():
            return f"{sign}{int(scaled_value)}{prefixes[exponent]}"
        else:
            return f"{sign}{scaled_value:.2f}{prefixes[exponent]}"
    else:
        if scaled_value.is_integer():
            return f"{sign}{int(scaled_value)}e{exponent}"
        else:
            return f"{sign}{scaled_value:.2f}e{exponent}"

class SvgFilterRenderer:
    """
        A class to create and manage SVG drawings for filter circuits.

        Attributes:
            dwg (svgwrite.Drawing): The SVG drawing object used for creating the SVG output.
            x (int): The x-coordinate for positioning elements in the drawing.
            y (int): The y-coordinate for positioning elements in the drawing.
            hasStart (bool): A flag indicating if the circuit has a starting component.
            hasEnd (bool): A flag indicating if the circuit has an ending component.

        Methods:
            __init__(x=0, y=0, filename='output.svg'): Initializes a new FiltersSvg instance.
    """

    def __init__(self, x: int=0, y: int=0, margin_x: int=0, margin_y: int=0, filename: str='output.svg'):
        """
            Initializes a new SvgFilterRenderer instance.

            Args:
                x (int, optional): The initial x-coordinate for positioning elements in the drawing. Defaults to 0.
                y (int, optional): The initial y-coordinate for positioning elements in the drawing. Defaults to 0.
                filename (str, optional): The name of the output SVG file. Defaults to 'output.svg'.
        """

        self.dwg = svgwrite.Drawing(filename, profile='tiny')
        self.x = x
        self.margin_x = margin_x
        self.y = y
        self.margin_y = margin_y
        self.hasStart = False
        self.hasFirstOrder = False
        self.hasEnd = False

    def add_start (self) -> None:
        """
            Adds a signal input to the circuit.

            This function creates a visual representation of a voltage input labeled 'Vin' in the circuit drawing.

            Args:
                This function does not take any arguments.

            Returns:
                None: This function does not return a value.
        """

        self.dwg.add(self.dwg.text(
            'Vin',
            insert=(self.x + 30, self.y + 12),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="end"
        ))

        self.dwg.add(self.dwg.circle(
            center=(self.x + 40, self.y + 6),
            r=4,
            fill="none",
            stroke="black",
            stroke_width = 2
        ))

        self.x += 44
        self.y += 6
        self.hasStart = True

        pass

    def add_low_pass_1 (self, r: float|int, c: float|int) -> None:
        """
            Adds a first order low-pass Sallen-Key filter to the circuit.

            Args:
                r (float or int): Frequency-defining resistor (ohms).
                c (float or int): Frequency-defining capacitor (farads).

            Returns:
                None: This function does not return a value.
        """

        if not self.hasStart:
            self.add_start()

        if self.y < 30:
            group = self.dwg.g(transform=f"translate(0 , {30 - self.y})")

            self.y = 0

            for element in self.dwg.elements:
                group.add(element)

            self.dwg.elements.clear()

            self.dwg.add(group)
        else:
            self.y = self.y - 30

        self.dwg.add(self.dwg.text(
            eng_format(r),
            insert=(self.x + 45, self.y + 15),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="middle"
        ))

        self.dwg.add(self.dwg.polyline(
            points=[
                (self.x + 0, self.y + 30),
                (self.x + 30, self.y + 30),
                (self.x + 35, self.y + 40),
                (self.x + 40, self.y + 20),
                (self.x + 45, self.y + 40),
                (self.x + 50, self.y + 20),
                (self.x + 55, self.y + 40),
                (self.x + 60, self.y + 20),
                (self.x + 65, self.y + 30),
                (self.x + 70, self.y + 30),
                (self.x + 160, self.y + 30)
            ],
            fill="none",
            stroke="black",
            stroke_linecap="round",
            stroke_linejoin="round",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.text(
            eng_format(c),
            insert=(self.x + 80, self.y + 80),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="end"
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 100, self.y + 30),
            end=(self.x + 100, self.y + 70),
            stroke="black",
            stroke_width=2,
            stroke_linecap="round"
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 85, self.y + 70),
            end=(self.x + 115, self.y + 70),
            stroke="black",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 85, self.y + 80),
            end=(self.x + 115, self.y + 80),
            stroke="black",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 100, self.y + 120),
            end=(self.x + 100, self.y + 80),
            stroke="black",
            stroke_width=2,
            stroke_linecap="round"
        ))

        self.dwg.add(self.dwg.polygon(
            points=[
                (self.x + 90, self.y + 120),
                (self.x + 100, self.y + 130),
                (self.x + 110, self.y + 120)
            ],
            fill="none",
            stroke="black",
            stroke_linejoin="round",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.text(
            '+',
            insert=(self.x + 170, self.y + 39),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=26,
            text_anchor = "middle"
        ))

        self.dwg.add(self.dwg.text(
            '-',
            insert=(self.x + 170, self.y + 78),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=26,
            text_anchor="middle"
        ))

        self.dwg.add(self.dwg.polygon(
            points=[
                (self.x + 160, self.y + 5),
                (self.x + 160, self.y + 95),
                (self.x + 250, self.y + 55)
            ],
            fill="none",
            stroke="black",
            stroke_linejoin="round",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.polyline(
            points=[
                (self.x + 160, self.y + 70),
                (self.x + 130, self.y + 70),
                (self.x + 130, self.y + 120),
                (self.x + 280, self.y + 120),
                (self.x + 280, self.y + 55),
                (self.x + 250, self.y + 55)
            ],
            fill="none",
            stroke="black",
            stroke_linecap="round",
            stroke_linejoin="round",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.circle(
            center=(self.x + 100, self.y + 30),
            r=4,
            fill="black",
            stroke="black"
        ))

        self.dwg.add(self.dwg.circle(
            center=(self.x + 280, self.y + 55),
            r=4,
            fill="black",
            stroke="black"
        ))

        self.x += 280
        self.y += 55

        pass

    def add_low_pass_2 (self, r: float|int, c: float|int, ra: float|int, rb: float|int) -> None:
        """
            Adds a low-pass Sallen-Key filter to the circuit.

            Args:
                r (float or int): Frequency-defining resistor (ohms).
                c (float or int): Frequency-defining capacitor (farads).
                ra (float or int): Resistor A, part of the gain adjustment (ohms).
                rb (float or int): Resistor B, part of the gain adjustment (ohms).

            Returns:
                None: This function does not return a value.
        """

        if not self.hasStart:
            self.add_start()

        if self.y < 90:
            group = self.dwg.g(transform=f"translate(0 , {90 - self.y})")

            self.y = 0

            for element in self.dwg.elements:
                group.add(element)

            self.dwg.elements.clear()

            self.dwg.add(group)
        else:
            self.y = self.y - 90

        self.dwg.add(self.dwg.text(
            eng_format(r),
            insert=(self.x + 45, self.y + 72),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="middle"
        ))

        self.dwg.add(self.dwg.text(
            eng_format(r),
            insert=(self.x + 150, self.y + 72),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="middle"
        ))

        self.dwg.add(self.dwg.polyline(
            points=[
                (self.x + 0, self.y + 90),
                (self.x + 30, self.y + 90),
                (self.x + 35, self.y + 100),
                (self.x + 40, self.y + 80),
                (self.x + 45, self.y + 100),
                (self.x + 50, self.y + 80),
                (self.x + 55, self.y + 100),
                (self.x + 60, self.y + 80),
                (self.x + 65, self.y + 90),
                (self.x + 70, self.y + 90),
                (self.x + 130, self.y + 90),
                (self.x + 135, self.y + 90),
                (self.x + 140, self.y + 100),
                (self.x + 145, self.y + 80),
                (self.x + 150, self.y + 100),
                (self.x + 155, self.y + 80),
                (self.x + 160, self.y + 100),
                (self.x + 165, self.y + 80),
                (self.x + 170, self.y + 90),
                (self.x + 260, self.y + 90)
            ],
            fill="none",
            stroke="black",
            stroke_linecap="round",
            stroke_linejoin="round",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.text(
            eng_format(c),
            insert=(self.x + 180, self.y + 142),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="end"
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 200, self.y + 90),
            end=(self.x + 200, self.y + 130),
            stroke="black",
            stroke_width=2,
            stroke_linecap="round"
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 185, self.y + 130),
            end=(self.x + 215, self.y + 130),
            stroke="black",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 185, self.y + 140),
            end=(self.x + 215, self.y + 140),
            stroke="black",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 200, self.y + 180),
            end=(self.x + 200, self.y + 140),
            stroke="black",
            stroke_width=2,
            stroke_linecap="round"
        ))

        self.dwg.add(self.dwg.polygon(
            points=[
                (self.x + 190, self.y + 180),
                (self.x + 200, self.y + 190),
                (self.x + 210, self.y + 180)
            ],
            fill="none",
            stroke="black",
            stroke_linejoin="round",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.text(
            '+',
            insert=(self.x + 270, self.y + 99),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=26,
            text_anchor = "middle"
        ))

        self.dwg.add(self.dwg.text(
            '-',
            insert=(self.x + 270, self.y + 138),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=26,
            text_anchor="middle"
        ))

        self.dwg.add(self.dwg.polygon(
            points=[
                (self.x + 260, self.y + 65),
                (self.x + 260, self.y + 155),
                (self.x + 350, self.y + 115)
            ],
            fill="none",
            stroke="black",
            stroke_linejoin="round",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.polyline(
            points=[
                (self.x + 260, self.y + 130),
                (self.x + 230, self.y + 130),
                (self.x + 230, self.y + 180),
                (self.x + 285, self.y + 180),
                (self.x + 290, self.y + 190),
                (self.x + 295, self.y + 170),
                (self.x + 300, self.y + 190),
                (self.x + 305, self.y + 170),
                (self.x + 310, self.y + 190),
                (self.x + 315, self.y + 170),
                (self.x + 320, self.y + 180),
                (self.x + 380, self.y + 180),
                (self.x + 380, self.y + 35),
                (self.x + 305, self.y + 35)
            ],
            fill="none",
            stroke="black",
            stroke_linecap="round",
            stroke_linejoin="round",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.polyline(
            points=[
                (self.x + 230, self.y + 180),
                (self.x + 230, self.y + 210),
                (self.x + 220, self.y + 215),
                (self.x + 240, self.y + 220),
                (self.x + 220, self.y + 225),
                (self.x + 240, self.y + 230),
                (self.x + 220, self.y + 235),
                (self.x + 240, self.y + 240),
                (self.x + 230, self.y + 245),
                (self.x + 230, self.y + 275)
            ],
            fill="none",
            stroke="black",
            stroke_width=2,
            stroke_linecap="round",
            stroke_linejoin="round"
        ))

        self.dwg.add(self.dwg.polygon(
            points=[
                (self.x + 220, self.y + 275),
                (self.x + 230, self.y + 285),
                (self.x + 240, self.y + 275)
            ],
            fill="none",
            stroke="black",
            stroke_linejoin="round",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.text(
            eng_format(rb), insert=(self.x + 305, self.y + 210),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="middle"
        ))

        self.dwg.add(self.dwg.text(
            eng_format(ra),
            insert=(self.x + 245, self.y + 235),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="start"
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 305, self.y + 50),
            end=(self.x + 305, self.y + 20),
            stroke="black",
            stroke_width=2,
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 295, self.y + 50),
            end=(self.x + 295, self.y + 20),
            stroke="black",
            stroke_width=2,
        ))

        self.dwg.add(self.dwg.polyline(
            points=[
                (self.x + 100, self.y + 90),
                (self.x + 100, self.y + 35),
                (self.x + 295, self.y + 35)
            ],
            fill="none",
            stroke="black",
            stroke_width=2,
            stroke_linecap="round",
            stroke_linejoin="round"
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 350, self.y + 115),
            end=(self.x + 380, self.y + 115),
            stroke="black",
            stroke_width=2,
            stroke_linecap="round"
        ))

        self.dwg.add(self.dwg.text(
            eng_format(c),
            insert=(self.x + 300, self.y + 15),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="middle"
        ))

        self.dwg.add(self.dwg.circle(
            center=(self.x + 100, self.y + 90),
            r=4,
            fill="black",
            stroke="black"
        ))

        self.dwg.add(self.dwg.circle(
            center=(self.x + 200, self.y + 90),
            r=4,
            fill="black",
            stroke="black"
        ))

        self.dwg.add(self.dwg.circle(
            center=(self.x + 230, self.y + 180),
            r=4,
            fill="black",
            stroke="black"
        ))

        self.dwg.add(self.dwg.circle(
            center=(self.x + 380, self.y + 115),
            r=4,
            fill="black",
            stroke="black"
        ))

        self.x += 380
        self.y += 115

        pass

    def add_high_pass (self, r: float|int, c: float|int, ra: float|int, rb: float|int) -> None:
        """
            Adds a high-pass Sallen-Key filter to the circuit.

            Args:
                r (float or int): Frequency-defining resistor (ohms).
                c (float or int): Frequency-defining capacitor (farads).
                ra (float or int): Resistor A, part of the gain adjustment (ohms).
                rb (float or int): Resistor B, part of the gain adjustment (ohms).

            Returns:
                None: This function does not return a value.
        """

        if not self.hasStart:
            self.add_start()

        if self.y < 90:
            group = self.dwg.g(transform=f"translate(0 , 90)")

            for element in self.dwg.elements:
                group.add(element)

            self.dwg.elements.clear()

            self.dwg.add(group)
        else:
            self.y = self.y - 90

        self.dwg.add(self.dwg.text(
            eng_format(c),
            insert=(self.x + 45, self.y + 70),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="middle"
        ))

        self.dwg.add(self.dwg.text(
            eng_format(c),
            insert=(self.x + 150, self.y + 70),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="middle"
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 0, self.y + 90),
            end=(self.x + 40, self.y + 90),
            stroke="black",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 40, self.y + 75),
            end=(self.x + 40, self.y + 105),
            stroke="black",
            stroke_width=2,
            stroke_linecap="round"
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 50, self.y + 75),
            end=(self.x + 50, self.y + 105),
            stroke="black",
            stroke_width=2,
            stroke_linecap="round"
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 50, self.y + 90),
            end=(self.x + 145, self.y + 90),
            stroke="black",
            stroke_width=2,
            stroke_linecap="round"
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 155, self.y + 90),
            end=(self.x + 260, self.y + 90),
            stroke="black",
            stroke_width=2,
            stroke_linecap="round"
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 145, self.y + 75),
            end=(self.x + 145, self.y + 105),
            stroke="black",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 155, self.y + 75),
            end=(self.x + 155, self.y + 105),
            stroke="black",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.text(
            eng_format(r),
            insert=(self.x + 180, self.y + 145),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="end"
        ))

        self.dwg.add(self.dwg.polyline(
            points=[
                (self.x + 200, self.y + 90),
                (self.x + 200, self.y + 120),
                (self.x + 190, self.y + 125),
                (self.x + 210, self.y + 130),
                (self.x + 190, self.y + 135),
                (self.x + 210, self.y + 140),
                (self.x + 190, self.y + 145),
                (self.x + 210, self.y + 150),
                (self.x + 200, self.y + 155),
                (self.x + 200, self.y + 185)
            ],
            fill="none",
            stroke="black",
            stroke_width=2,
            stroke_linecap="round",
            stroke_linejoin="round"
        ))

        self.dwg.add(self.dwg.polygon(
            points=[
                (self.x + 190, self.y + 185),
                (self.x + 200, self.y + 195),
                (self.x + 210, self.y + 185)
            ],
            fill="none",
            stroke="black",
            stroke_linejoin="round",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.text(
            '+',
            insert=(self.x + 270, self.y + 99),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=26,
            text_anchor = "middle"
        ))

        self.dwg.add(self.dwg.text(
            '-',
            insert=(self.x + 270, self.y + 138),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=26,
            text_anchor="middle"
        ))

        self.dwg.add(self.dwg.polygon(
            points=[
                (self.x + 260, self.y + 65),
                (self.x + 260, self.y + 155),
                (self.x + 350, self.y + 115)
            ],
            fill="none",
            stroke="black",
            stroke_linejoin="round",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.polyline(
            points=[
                (self.x + 260, self.y + 130),
                (self.x + 230, self.y + 130),
                (self.x + 230, self.y + 180),
                (self.x + 285, self.y + 180),
                (self.x + 290, self.y + 190),
                (self.x + 295, self.y + 170),
                (self.x + 300, self.y + 190),
                (self.x + 305, self.y + 170),
                (self.x + 310, self.y + 190),
                (self.x + 315, self.y + 170),
                (self.x + 320, self.y + 180),
                (self.x + 380, self.y + 180),
                (self.x + 380, self.y + 35),
                (self.x + 320, self.y + 35),
                (self.x + 315, self.y + 25),
                (self.x + 310, self.y + 45),
                (self.x + 305, self.y + 25),
                (self.x + 300, self.y + 45),
                (self.x + 295, self.y + 25),
                (self.x + 290, self.y + 45),
                (self.x + 285, self.y + 35),
                (self.x + 100, self.y + 35),
                (self.x + 100, self.y + 90)
            ],
            fill="none",
            stroke="black",
            stroke_linecap="round",
            stroke_linejoin="round",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.polyline(
            points=[
                (self.x + 230, self.y + 180),
                (self.x + 230, self.y + 210),
                (self.x + 220, self.y + 215),
                (self.x + 240, self.y + 220),
                (self.x + 220, self.y + 225),
                (self.x + 240, self.y + 230),
                (self.x + 220, self.y + 235),
                (self.x + 240, self.y + 240),
                (self.x + 230, self.y + 245),
                (self.x + 230, self.y + 275)
            ],
            fill="none",
            stroke="black",
            stroke_width=2,
            stroke_linecap="round",
            stroke_linejoin="round"
        ))

        self.dwg.add(self.dwg.polygon(
            points=[
                (self.x + 220, self.y + 275),
                (self.x + 230, self.y + 285),
                (self.x + 240, self.y + 275)
            ],
            fill="none",
            stroke="black",
            stroke_linejoin="round",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.text(
            eng_format(rb),
            insert=(self.x + 300, self.y + 210),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="middle"
        ))

        self.dwg.add(self.dwg.text(
            eng_format(ra),
            insert=(self.x + 245, self.y + 235),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="start"
        ))

        self.dwg.add(self.dwg.line(
            start=(self.x + 350, self.y + 115),
            end=(self.x + 410, self.y + 115),
            stroke="black",
            stroke_width=2,
            stroke_linecap="round"
        ))

        self.dwg.add(self.dwg.text(
            eng_format(r),
            insert=(self.x + 300, self.y + 17),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="middle"
        ))

        self.dwg.add(self.dwg.circle(
            center=(self.x + 100, self.y + 90),
            r=4,
            fill="black",
            stroke="black"
        ))

        self.dwg.add(self.dwg.circle(
            center=(self.x + 200, self.y + 90),
            r=4,
            fill="black",
            stroke="black"
        ))

        self.dwg.add(self.dwg.circle(
            center=(self.x + 230, self.y + 180),
            r=4,
            fill="black",
            stroke="black"
        ))

        self.dwg.add(self.dwg.circle(
            center=(self.x + 380, self.y + 115),
            r=4,
            fill="black",
            stroke="black"
        ))

        self.x += 410
        self.y += 115

    def add_gain_adjustment(self, rx: float|int, ry: float|int) -> None:
        if not self.hasStart:
            self.add_start()

        if self.y < 30:
            group = self.dwg.g(transform=f"translate(0 , {30 - self.y})")

            self.y = 0

            for element in self.dwg.elements:
                group.add(element)

            self.dwg.elements.clear()

            self.dwg.add(group)
        else:
            self.y = self.y - 30

        self.dwg.add(self.dwg.text(
            eng_format(rx),
            insert=(self.x + 45, self.y + 15),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="middle"
        ))

        self.dwg.add(self.dwg.text(
            eng_format(ry),
            insert=(self.x + 115, self.y + 85),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="start"
        ))

        self.dwg.add(self.dwg.polyline(
            points=[
                (self.x + 0, self.y + 30),
                (self.x + 30, self.y + 30),
                (self.x + 35, self.y + 40),
                (self.x + 40, self.y + 20),
                (self.x + 45, self.y + 40),
                (self.x + 50, self.y + 20),
                (self.x + 55, self.y + 40),
                (self.x + 60, self.y + 20),
                (self.x + 65, self.y + 30),
                (self.x + 70, self.y + 30),
                (self.x + 100, self.y + 30),
                (self.x + 100, self.y + 60),
                (self.x + 90, self.y + 65),
                (self.x + 110, self.y + 70),
                (self.x + 90, self.y + 75),
                (self.x + 110, self.y + 80),
                (self.x + 90, self.y + 85),
                (self.x + 110, self.y + 90),
                (self.x + 100, self.y + 95),
                (self.x + 100, self.y + 125)

            ],
            fill="none",
            stroke="black",
            stroke_linecap="round",
            stroke_linejoin="round",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.polygon(
            points=[
                (self.x + 90, self.y + 125),
                (self.x + 100, self.y + 135),
                (self.x + 110, self.y + 125)
            ],
            fill="none",
            stroke="black",
            stroke_linejoin="round",
            stroke_width=2
        ))

        self.dwg.add(self.dwg.circle(
            center=(self.x + 100, self.y + 30),
            r=4,
            fill="black",
            stroke="black"
        ))

        self.x += 100
        self.y += 30

        pass

    def add_end (self) -> None:
        """
            Adds a signal output to the circuit.

            This function creates a visual representation of a voltage output labeled 'Vout' in the circuit drawing.

            Args:
                This function does not take any arguments.

            Returns:
                None: This function does not return a value.
        """

        self.dwg.add(self.dwg.line(
            start=(self.x + 0, self.y + 0),
            end=(self.x + 30, self.y + 0),
            stroke="black",
            stroke_width=2,
            stroke_linecap="round"
        ))

        self.dwg.add(self.dwg.circle(
            center=(self.x + 34, self.y + 0),
            r=4,
            fill="none",
            stroke="black",
            stroke_width = 2
        ))

        self.dwg.add(self.dwg.text(
            'Vout',
            insert=(self.x + 40, self.y + 5),
            fill="black",
            font_family="Arial, sans-serif",
            font_size=20,
            text_anchor="start"
        ))

        self.x += 85
        self.y += 0
        self.hasEnd = True

        pass

    def get_dwg(self) -> svgwrite:
        """
            Retrieves the drawing object.

            This function returns the current SVG drawing object associated with the instance.

            Args:
                This function does not take any arguments.

            Returns:
                svgwrite: The SVG drawing object.
        """

        return self.dwg

    def save_dwg(self) -> None:
        """
            Saves the current SVG drawing.

            This function checks if the drawing has an ending component; if not, it adds one
            before saving the SVG drawing object.

            Args:
                This function does not take any arguments.

            Returns:
                None: This function does not return a value.
        """

        if not self.hasEnd:
            self.add_end()

        self.dwg.update({"width": self.x, "height": self.y + 171})

        return self.dwg.save()