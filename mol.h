/*
File Owned By: Wali Temuri 1183379
CIS - 2750 A1
Email: wtemuri@uoguelph.ca
Date Created: 01-10-2023
*/
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

/*
    Structure: Atom

    DataTypes:
        char element => string representing element name of atom
        double x,y,z => doubles representing the position of the atom relative
   to a common origin for a molecule
*/

typedef struct atom {
    char element[3];
    double x, y, z;
} atom;

/*
    Structure: Bond

    DataTypes:
        unsigned short a1, a2 => indices of the two atoms in the covalent bond
   within an array with address atoms. atoms[a1], atoms[a2] unsigned char epairs
   represents the number of elements in the bond double x1y1,x2,y2 will store
   the coordinates of atoms a1 and a2 respectively double z will store the
   average z value between atoms a1 and a2. double len will store the distance
   from a1 to a2 double dx and dy will store the differences between the x and y
   values of a2 and a1 / length of the bond


*/
typedef struct bond {
    unsigned short a1, a2;
    unsigned char epairs;
    atom *atoms;
    double x1, x2, y1, y2, z, len, dx, dy;
} bond;

/*
    Structure: Molecule

    DataTypes:
        unsigned short atom_max, atom_no =>
            atom_max: non-negative int that represents array dimensionality of
   atoms atom_no: number of atoms stored in array atoms (Note: Must Always be <
   atom_max) atom *atoms, **atom_ptrs unsigned short bond_max, bond_no bond
   *bonds, **bond_ptrs
*/
typedef struct molecule {
    unsigned short atom_max, atom_no;
    atom *atoms, **atom_ptrs;
    unsigned short bond_max, bond_no;
    bond *bonds, **bond_ptrs;
} molecule;

typedef double xform_matrix[3][3];

void atomset(atom *atom, char element[3], double *x, double *y, double *z);
void atomget(atom *atom, char element[3], double *x, double *y, double *z);
void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms,
             unsigned char *epairs);
void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms,
             unsigned char *epairs);
molecule *molmalloc(unsigned short atom_max, unsigned short bond_max);
molecule *molcopy(molecule *src);
void molfree(molecule *ptr);
void molappend_atom(molecule *molecule, atom *atom);
void molappend_bond(molecule *molecule, bond *bond);
void molsort(molecule *molecule);
void xrotation(xform_matrix xform_matrix, unsigned short deg);
void yrotation(xform_matrix xform_matrix, unsigned short deg);
void zrotation(xform_matrix xform_matrix, unsigned short deg);
void mol_xform(molecule *molecule, xform_matrix matrix);
void compute_coords(bond *bond);
int bond_comp(const void *a, const void *b);
int compareAtoms(const void *a, const void *b);
