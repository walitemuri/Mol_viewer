import molecule
import molsql
header = """<svg version="1.1" width="1000" height="1000"
                        xmlns="http://www.w3.org/2000/svg">"""

footer = """</svg>"""

offsetx = 500
offsety = 500


class Atom():
    def __init__(self, c_atom):
        self.atom = c_atom
        self.z = self.atom.z

    def __str__(self):
        return f"{self.atom.element}, {self.atom.x}, {self.atom.y}, {self.z}"

    def svg(self):
        return ' <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (100.0 * self.atom.x + offsetx, self.atom.y * 100.0 + offsety, radius[self.atom.element], element_name[self.atom.element])


class Bond():
    def __init__(self, c_bond):
        self.bond = c_bond
        self.z = self.bond.z

    def __str__(self):
        return f"{self.bond.a1}, {self.bond.a2}, {self.bond.epairs}, {self.bond.x1}, {self.bond.y1}, {self.bond.x2}, {self.bond.y2}, {self.bond.len}, {self.bond.dx}, {self.bond.dy}"

    def svg(self):
        # calculate atoms x and y coordinates
        a1_x, a1_y = self.bond.x1 * 100 + offsetx, self.bond.y1 * 100 + offsety
        a2_x, a2_y = self.bond.x2 * 100 + offsetx, self.bond.y2 * 100 + offsety

        # calculate positive and negative x values if dy is not 0
        x1_pos, x1_neg = a1_x + self.bond.dy * 10, a1_x - \
            self.bond.dy * 10 if self.bond.dy != 0 else (a1_x, a1_x)
        x2_pos, x2_neg = a2_x + self.bond.dy * 10, a2_x - \
            self.bond.dy * 10 if self.bond.dy != 0 else (a2_x, a2_x)

        # calculate positive and negative y values if dx is not 0
        y1_pos, y1_neg = a1_y + self.bond.dx * 10, a1_y - \
            self.bond.dx * 10 if self.bond.dx != 0 else (a1_y, a1_y)
        y2_pos, y2_neg = a2_y + self.bond.dx * 10, a2_y - \
            self.bond.dx * 10 if self.bond.dx != 0 else (a2_y, a2_y)

        return f'  <polygon points="{x1_neg:.2f},{y1_pos:.2f} {x1_pos:.2f},{y1_neg:.2f} {x2_pos:.2f},{y2_neg:.2f} {x2_neg:.2f},{y2_pos:.2f}" stroke="black"/>\n'


class Molecule(molecule.molecule):
    def __init__(self):
        super().__init__()

    def __str__(self):
        pass

    def svg(self):
        atoms = []
        bonds = []

        for i in range(self.atom_no):
            atom = self.get_atom(i)
            atoms.append(Atom(atom))
        for i in range(self.bond_no):
            bond = self.get_bond(i)
            bonds.append(Bond(bond))

        svg_str = header

        while atoms and bonds:
            a1 = atoms[0]
            b1 = bonds[0]
            if a1.z < b1.z:
                svg_str += a1.svg()
                atoms.pop(0)
            else:
                svg_str += b1.svg()
                bonds.pop(0)

        while atoms:
            a1 = atoms.pop(0)
            svg_str += a1.svg()

        while bonds:
            b1 = bonds.pop(0)
            svg_str += b1.svg()

        svg_str += footer

        return svg_str

    def parse(self, fileobj):
        # print("Enerterd function")
        lines = fileobj.readlines()

        atom_no = int(lines[3].split()[0])
        bond_no = int(lines[3].split()[1])

        for i in range(atom_no):
            # print(i)
            line = lines[4 + i]
            x = float(line[0:10])
            y = float(line[10:20])
            z = float(line[20:30])
            element = line[31]
            # print(x , y, z , element)
            self.append_atom(element, x, y, z)

        # print(" atom done ")
        for i in range(bond_no):
            line = lines[4 + i + atom_no]
            token = line.split()
            # print(token[0], token[1], token[2])
            self.append_bond(int(token[0]) - 1, int(token[1]) - 1, int(
                token[2]))  # set bond info to tokens
