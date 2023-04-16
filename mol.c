/*
File Owned By: Wali Temuri
Email: wtemuri@uoguelph.ca
Date Created: 01-10-2023
*/

#include "mol.h"
#define EPSILON 0.000001

void atomset(atom *atom, char element[3], double *x, double *y, double *z) {
    if (atom == NULL) {
        printf("Error: Invalid atom\n");
        return;
    }

    strcpy(atom->element, element);
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
}

void atomget(atom *atom, char element[3], double *x, double *y, double *z) {
    if (atom == NULL) {
        printf("Error: atom is NULL\n");
        return;
    }

    strcpy(element, atom->element);
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
}

void compute_coords(bond *bond) {
    atom *a1 = &bond->atoms[bond->a1];
    atom *a2 = &bond->atoms[bond->a2];

    if (a1 == NULL || a2 == NULL) {
        printf("Exception: atom at index is NULL\n");
        return;
    }

    bond->z = (a1->z + a2->z) / 2.0;
    bond->x1 = a1->x;
    bond->y1 = a1->y;
    bond->x2 = a2->x;
    bond->y2 = a2->y;
    bond->len = sqrt(((a2->x - a1->x) * (a2->x - a1->x)) +
                     ((a2->y - a1->y) * (a2->y - a1->y)));
    bond->dx = (a2->x - a1->x) / bond->len;
    bond->dy = (a2->y - a1->y) / bond->len;
}

void bondset(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms,
             unsigned char *epairs) {
    if (a1 == a2) {
        printf("indices of two atoms cannot be the same\n");
        return;
    }

    if (*atoms == NULL) {
        printf("atoms array is empty\n");
        return;
    }

    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->atoms = *atoms;
    bond->epairs = *epairs;
    compute_coords(bond);
}

void bondget(bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms,
             unsigned char *epairs) {
    *a1 = bond->a1;
    *a2 = bond->a2;
    *epairs = bond->epairs;
    *atoms = bond->atoms;
}

/*
Function: molmallloc
In: unsigned short atom_max, unsigned short bond_max
Out: molecule *
Post: returns address of the molecule after allocating sufficient memory
*/
molecule *molmalloc(unsigned short atom_max, unsigned short bond_max) {
    molecule *node = NULL;

    node = malloc(sizeof(molecule));
    node->atom_no = 0;
    node->bond_no = 0;
    node->bond_max = bond_max;
    node->atom_max = atom_max;

    if (atom_max == 0 || bond_max == 0) {
        return node;
    } else {
        // malloced to have enough memory respectively
        node->atoms = (atom *)malloc(sizeof(atom) * atom_max);
        node->atom_ptrs = (atom **)malloc(sizeof(atom *) * atom_max);

        node->bonds = (bond *)malloc(sizeof(bond) * bond_max);
        node->bond_ptrs = (bond **)malloc(sizeof(bond *) * bond_max);
    }
    return node;
}

/*
Function: molcopy
In: molecule * src
Out: molecule *
Post: Copies a molecule and returns the address of the new molecule
*/
molecule *molcopy(molecule *src) {
    if (src == NULL) {
        printf("src molecule is NULL\n");
        return NULL;
    }

    molecule *newMol = molmalloc(src->atom_max, src->bond_max);

    if (newMol == NULL) {
        printf("malloc error\n");
        return NULL;
    }

    for (int i = 0; i < src->atom_no; i++) {
        molappend_atom(newMol, &src->atoms[i]);
    }
    for (int i = 0; i < src->bond_no; i++) {

        molappend_bond(newMol, &src->bonds[i]);
    }

    return newMol;
}

void molfree(molecule *ptr) {
    if (ptr == NULL) {
        printf("Can't Free NULL ptr\n");
        return;
    }

    if (ptr->atoms != NULL) {
        free(ptr->atoms);
    }
    if (ptr->atom_ptrs != NULL) {
        free(ptr->atom_ptrs);
    }

    if (ptr->bonds != NULL) {
        free(ptr->bonds);
    }

    if (ptr->bond_ptrs != NULL) {
        free(ptr->bond_ptrs);
    }
    free(ptr);
}

/*
Function: molappend_atom
In: molecule * molecule, atom * new_atom
Out: void
Post: Appends the atom to the molecule array
*/
void molappend_atom(molecule *molecule, atom *new_atom) {
    if (molecule == NULL) {
        printf("molecule is NULL\n");
        return;
    } else if (new_atom == NULL) {
        printf("new_atom is NULL\n");
        return;
    }

    if (molecule->atom_max == molecule->atom_no) {
        if (molecule->atom_max == 0) {
            ++molecule->atom_max;
            molecule->atoms = (atom *)malloc(sizeof(atom) * molecule->atom_max);
            molecule->atom_ptrs =
                (atom **)malloc(sizeof(atom *) * molecule->atom_max);

            if (molecule->atom_ptrs == NULL || molecule->atoms == NULL) {
                printf("Error: Unable to allocate\n");
                return;
            }
        } else {
            molecule->atom_max *= 2;
            molecule->atoms = (atom *)realloc(
                molecule->atoms, sizeof(atom) * molecule->atom_max);
            molecule->atom_ptrs = (atom **)realloc(
                molecule->atom_ptrs, sizeof(atom *) * molecule->atom_max);

            if (molecule->atom_ptrs == NULL || molecule->atoms == NULL) {
                printf("Error: Unable to allocate\n");
                return;
            }
        }
    }

    memcpy(&molecule->atoms[molecule->atom_no], new_atom, sizeof(atom));
    molecule->atom_no++;

    /* Sets pointers array to point at all atoms */

    for (int i = 0; i < molecule->atom_no; i++) {
        molecule->atom_ptrs[i] = &molecule->atoms[i];
    }
}

/*
Function: molappend_bond
In: molecule * molecule, bond * new_bond
Out: void
Post: Appends the bond to the molecule passed in
*/
void molappend_bond(molecule *molecule, bond *new_bond) {
    if (molecule == NULL) {
        printf("molecule is NULL\n");
        return;
    } else if (new_bond == NULL) {
        printf("new_bond is NULL\n");
        return;
    }

    if (molecule->bond_max == molecule->bond_no) {
        if (molecule->bond_max == 0) {
            ++molecule->bond_max;
            molecule->bonds = (bond *)malloc(sizeof(bond) * molecule->bond_max);
            molecule->bond_ptrs =
                (bond **)malloc(sizeof(bond *) * molecule->bond_max);

            if (molecule->bond_ptrs == NULL || molecule->bonds == NULL) {
                printf("Error: Unable to allocate\n");
                return;
            }
        } else {
            molecule->bond_max *= 2;
            molecule->bonds =
                realloc(molecule->bonds, sizeof(bond) * molecule->bond_max);
            molecule->bond_ptrs = realloc(molecule->bond_ptrs,
                                          sizeof(bond *) * molecule->bond_max);
        }
    }

    memcpy(&molecule->bonds[molecule->bond_no], new_bond, sizeof(bond));
    molecule->bond_no++;

    /* Sets pointers array to point at all bonds */
    for (int i = 0; i < molecule->bond_no; i++) {
        molecule->bond_ptrs[i] = &molecule->bonds[i];
    }
}

/*
Function: compareAtoms
In: const void *a , const void *b
Out: 1, -1 , 0
Post: Compares two elements of the atom array for Qsort algorithm
*/
int compareAtoms(const void *a, const void *b) {
    atom *firstAtom = *((atom **)a);
    atom *secondAtom = *((atom **)b);

    if (firstAtom->z == secondAtom->z) {
        return 0;
    } else if (firstAtom->z < secondAtom->z) {
        return -1;
    }

    return 1;
}

/*
Function: compareBonds
In: const void *a, const void *b
Out: 1,0,-1
Post: Compares two bonds for the Qsort algorithm
*/
int bond_comp(const void *a, const void *b) {
    bond *firstBond = *((bond **)a);
    bond *secondBond = *((bond **)b);

    if (firstBond->z == secondBond->z) {
        return 0;
    } else if (firstBond->z < secondBond->z) {
        return -1;
    }

    return 1;
}

/*
Function: molsort
In: molecule * molecule
Out: void
Post: Sorts both arrays bonds, and atoms by ascending Z values.
*/
void molsort(molecule *molecule) {
    if (molecule->atom_ptrs == NULL || molecule->bond_ptrs == NULL) {
        printf("molsort error: molecule contains Null atom or bond array\n");
        return;
    }

    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(atom *), compareAtoms);
    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(bond *), bond_comp);
}

/*
Function: xrotation
In: xform_matrix xform_matrix, unsigned short deg
Out: void
Post: Sets the affine transformation matrix for rotation around the X axis
*/
void xrotation(xform_matrix xform_matrix, unsigned short deg) {
    double theta = deg * M_PI / 180.0;
    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(theta);
    xform_matrix[1][2] = -sin(theta);
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(theta);
    xform_matrix[2][2] = cos(theta);
}

/*
Function: yrotation
In: xform_matrix xform_matrix, unsigned short deg
Out: void
Post: Sets the affine transformation matrix for rotation around the Y axis
*/
void yrotation(xform_matrix xform_matrix, unsigned short deg) {
    double theta = deg * M_PI / 180.0;

    xform_matrix[0][0] = cos(theta);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(theta);
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;
    xform_matrix[2][0] = -sin(theta);
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(theta);
}

/*
Function: zrotation
In: xform_matrix xform_matrix, unsigned short deg
Out: void
Post: Sets the affine transformation matrix for rotation around the Z axis
*/
void zrotation(xform_matrix xform_matrix, unsigned short deg) {
    double theta = deg * M_PI / 180.0;
    xform_matrix[0][0] = cos(theta);
    xform_matrix[0][1] = -sin(theta);
    xform_matrix[0][2] = 0;
    xform_matrix[1][0] = sin(theta);
    xform_matrix[1][1] = cos(theta);
    xform_matrix[1][2] = 0;
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
}

/*
Function: mol_xform
In: molecule * mol , xform matrix matrix
Out: void
Post: Multiplies each coordiante of the atoms in molecule by the transformation
matrix
*/
void mol_xform(molecule *mol, xform_matrix matrix) {
    if (mol == NULL || mol->atoms == NULL) {
        printf("Error: molecule is NULL or its atoms are NULL\n");
        return;
    }

    for (int i = 0; i < mol->atom_no; i++) {
        double x = mol->atom_ptrs[i]->x, y = mol->atom_ptrs[i]->y,
               z = mol->atom_ptrs[i]->z;

        mol->atom_ptrs[i]->x =
            matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z;
        mol->atom_ptrs[i]->y =
            matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z;
        mol->atom_ptrs[i]->z =
            matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z;
    }

    for (int i = 0; i < mol->bond_no; i++) {
        compute_coords(mol->bond_ptrs[i]);
    }
}

int main() {
    //    if (test_compute_coords_basic())
    //    {
    //         printf("Test Passed\n");
    //    }
    //    else
    //    {
    //     printf("Test Failed\n");
    //    }
    return 0;
}
