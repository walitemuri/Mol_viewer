CC = clang
CFLAGS = -Wall -std=c99 -pedantic
LIBS = -lm
PYTHON_HEADER_PATH = /usr/include/python3.7m
PYTHON_LIBRARY_PATH = /usr/lib/python3.7/config-3.7m-x86_64-linux-gnu

all:  libmol.so mol _molecule.so

mol: mol.o
	$(CC) $(CFLAGS) mol.o -L. -lmol -o mol $(LIBS)

libmol.so: mol.o
	$(CC) mol.o -shared -o libmol.so

mol.o:  mol.c mol.h
	$(CC) $(CFLAGS) -c mol.c -fPIC -o mol.o

_molecule.so: molecule_wrap.o libmol.so
	$(CC) molecule_wrap.o -shared -lpython3.7 -lmol -o _molecule.so -L. -L$(PYTHON_LIBRARY_PATH) -dynamiclib

molecule_wrap.o: molecule_wrap.c
	$(CC) $(CFLAGS) -I$(PYTHON_HEADER_PATH) -c molecule_wrap.c -fPIC -o molecule_wrap.o

clean:
	rm -f *.o *.so mol
