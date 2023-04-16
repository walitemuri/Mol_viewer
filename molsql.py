import sqlite3
import os
import MolDisplay


class Database:
    def __init__(self, reset=False):
        if reset and os.path.exists("./molecules.db"):
            os.remove("./molecules.db")
        self.conn = sqlite3.connect("molecules.db")
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Elements (
                            element_no INTEGER NOT NULL,
                            element_code VARCHAR(3) PRIMARY KEY NOT NULL,
                            element_name VARCHAR(32) NOT NULL,
                            colour1 CHAR(6) NOT NULL,
                            colour2 CHAR(6) NOT NULL,
                            colour3 CHAR(6) NOT NULL,
                            radius DECIMAL(3) NOT NULL)""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Atoms (
                            atom_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            element_code VARCHAR(3) REFERENCES Elements(element_code) NOT NULL,
                            x DECIMAL(7, 4) NOT NULL,
                            y DECIMAL(7, 4) NOT NULL,
                            z DECIMAL(7, 4) NOT NULL)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Bonds (
                            bond_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            a1 INTEGER NOT NULL,
                            a2 INTEGER NOT NULL,
                            epairs INTEGER NOT NULL)""")
        self.conn.commit()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Molecules (
                            molecule_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            name TEXT UNIQUE NOT NULL)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS MoleculeAtom (
                            molecule_id INTEGER REFERENCES Molecules(molecule_id) NOT NULL,
                            atom_id INTEGER REFERENCES Atoms(atom_id) NOT NULL)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS MoleculeBond (
                            molecule_id INTEGER REFERENCES Molecules(molecule_id) NOT NULL,
                            bond_id INTEGER REFERENCES Bonds(bond_id) NOT NULL)""")
        self.conn.commit()

    def __setitem__(self, table, values):
        SQL_STATEMENTS = {
            'Elements': 'INSERT INTO Elements (element_no, element_code, element_name, colour1, colour2, colour3, radius) VALUES (?, ?, ?, ?, ?, ?, ?)',
            'Atoms': 'INSERT INTO Atoms (element_code, x, y, Z) VALUES (?, ?, ?, ?)',
            'Bonds': 'INSERT INTO Bonds (a1, a2, epairs) VALUES (?, ?, ?)',
            'Molecules': 'INSERT INTO Molecules (name) VALUES (?)',
            'MoleculeAtom': 'INSERT INTO MoleculeAtom (molecule_id, atom_id) VALUES (?, ?)',
            'MoleculeBond': 'INSERT INTO MoleculeBond (molecule_id, bond_id) VALUES (?, ?)',
        }
        sql_statement = SQL_STATEMENTS.get(table)
        if sql_statement is None:
            raise ValueError(f'Table {table} not found in database')
        if table == 'Molecules':
            values = (values,)
        self.cursor.execute(sql_statement, values)
        self.conn.commit()

    def add_atom(self, mol_name, atom):
        self['Atoms'] = (atom.element, atom.x, atom.y, atom.z)
        atom_id = self.cursor.lastrowid
        molecule_id = self.cursor.execute(
            f"""SELECT molecule_id FROM Molecules WHERE name = '{ mol_name }'""").fetchone()[0]
        # print(atom_id, molecule_id)
        self['MoleculeAtom'] = (molecule_id, atom_id)

    def add_bond(self, mol_name, bond):
        self['Bonds'] = (bond.a1, bond.a2, bond.epairs)
        bond_id = self.cursor.lastrowid
        molecule_id = self.cursor.execute(
            f"""SELECT molecule_id FROM Molecules WHERE name = '{mol_name}'""").fetchone()[0]
        self['MoleculeBond'] = (molecule_id, bond_id)

    def add_molecule(self, name, fp):
        molecule = MolDisplay.Molecule()
        molecule.parse(fp)
        self['Molecules'] = (name)
        for i in range(molecule.atom_no):
            atom = molecule.get_atom(i)
            self.add_atom(name, atom)
        for i in range(molecule.bond_no):
            bond = molecule.get_bond(i)
            self.add_bond(name, bond)

    def load_mol(self, name):
        molecule = MolDisplay.Molecule()
        res = self.cursor.execute(
            f"""SELECT * FROM Molecules
                INNER JOIN MoleculeAtom
                ON Molecules.molecule_id = MoleculeAtom.molecule_id
                INNER JOIN Atoms
                ON MoleculeAtom.atom_id = Atoms.atom_id
                WHERE name = '{name}'
                ORDER BY atom_id""").fetchall()
        # res = sorted(res, key=lambda x: x[3])
        # print(res)
        for element in res:
            molecule.append_atom(
                element[5], element[6],  element[7], element[8])
        res = self.cursor.execute(
            f"""SELECT * FROM Molecules
                INNER JOIN MoleculeBond
                ON Molecules.molecule_id = MoleculeBond.molecule_id
                INNER JOIN Bonds
                ON MoleculeBond.bond_id = Bonds.bond_id
                WHERE name = '{name}'
                ORDER BY bond_id""").fetchall()
        for element in res:
            molecule.append_bond(
                element[5],  element[6], element[7])
        return molecule

    def radius(self):
        res = self.cursor.execute(
            """SELECT element_code, radius FROM Elements""").fetchall()
        my_dict = {x[0]: x[1] for x in res}
        return my_dict

    def element_name(self):
        res = self.cursor.execute(
            """SELECT element_code, element_name FROM Elements""").fetchall()
        my_dict = {x[0]: x[1] for x in res}
        return my_dict

    def radial_gradients(self):
        res = self.cursor.execute("""SELECT * FROM Elements""").fetchall()
        elems = ""
        for element in res:
            elems += '''radialGradientSVG = """
                            <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
                                <stop offset="0%%" stop-color="#%s"/>
                                <stop offset="50%%" stop-color="#%s"/>
                                <stop offset="100%%" stop-color="#%s"/>
                            </radialGradient>""";''' % (element[2], element[3], element[4], element[5])
        return elems

    def get_molecules(self):
        mols = []
        res = self.cursor.execute("""SELECT name FROM Molecules""").fetchall()
        for mol in res:
            moleculeObj = self.load_mol(mol[0])
            mols.append({"name": mol[0], "atoms": moleculeObj.atom_no, "bonds": moleculeObj.bond_no})
        print(mols)
        return mols

    def get_elements(self):
        query = "SELECT * FROM Elements"
        self.cursor.execute(query)
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def delete_element(self, id):
        query = f"DELETE FROM Elements WHERE element_no = {id}"
        item = self.cursor.execute(query).fetchone()
        self.conn.commit()
        print(item)
        return item
    
if __name__ == "__main__":
    db = Database(reset=True);
    db.create_tables();
    db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
    db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
    db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
    db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
    # fp = open( 'water-3D-structure-CT1000292221.sdf' );
    # db.add_molecule( 'Water', fp );
    # fp = open( 'caffeine-3D-structure-CT1001987571.sdf' );
    # db.add_molecule( 'Caffeine', fp );
    # fp = open( 'CID_31260.sdf' );
    # db.add_molecule( 'Isopentanol', fp );


    print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM Atoms;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM Bonds;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM MoleculeBond;" ).fetchall() );