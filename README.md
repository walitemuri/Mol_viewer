# Molecule Viewer: SDF Molecule Visualization Web Application

Author: Wali Temuri

## Description

MoleculeViewer is a powerful and efficient web application designed for scientists, researchers, and chemistry enthusiasts. It enables users to visualize and interact with molecular structures by parsing and rendering Structure Data File (SDF) formats with ease.

### Key Features

- SDF File Support: Seamlessly parse and render SDF files, a widely-used format for representing chemical compounds and their associated data.
- Interactive 3D Viewer: Explore and analyze molecular structures in detail with our intuitive 3D viewer. Rotate, zoom, and pan to gain a comprehensive understanding of each molecule.
- Element Upload: Conveniently upload custom elements and expand your molecular library, fostering a collaborative and dynamic research environment.
- Responsive Design: Optimized for both desktop and mobile devices, MoleculeViewer ensures a seamless experience across various platforms.
- Optimization: Uses low-level C program to perform fast computation requried to rotate the molecule asyncronously.

## Dependencies

- The current configuration is suited only for a Linux environemnt.

- Swig3.0 was used in development, no gurantee it will work with future versions.

## Getting Started

Firstly run the setup script using the following command:

```
./setup.sh
```

This should compile the C program, now you must run the server with your desired port.
```
python3 ajaxserver.py {port_num}
```

## Preview -- Coming Soon

