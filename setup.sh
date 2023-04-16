#!/bin/bash

# Run the swig3.0 command
swig3.0 -python molecule.i

# Set the LD_LIBRARY_PATH environment variable
export LD_LIBRARY_PATH=$(pwd)

# Run the make command
make
