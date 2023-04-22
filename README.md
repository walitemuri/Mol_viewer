# Molecule Viewer: SDF Molecule Visualization Web Application

Author: Wali Temuri

### Parse and render SDF files that you Upload
![Mol_Viewer_MolDisplay](https://user-images.githubusercontent.com/108627530/233803053-0c1cc534-e746-40f7-b3c1-acff81d6fb0b.gif)



### Delete and Add New Elements
![Mol_viewer_elementslist](https://user-images.githubusercontent.com/108627530/233802837-a011c34b-1ef6-4d76-805b-aacf44ec283b.gif)


## Description

MoleculeViewer is a powerful and efficient web application designed for scientists, researchers, and chemistry enthusiasts. It enables users to visualize and interact with molecular structures by parsing and rendering Structure Data File (SDF) formats with ease.

### Technologies Used

- C for low-level quick computation required for rotating molecules, sorting atoms, computing coordinates
- Python/SWIG in order to interface with C code and HTTPServer used for back-end server
- HTML/CSS for front-end design
- SQLite as the database to store molecule, atom, bond information
- Jquery/Ajax for requests to the back-end which Asynchronously updates the front-end interface

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

