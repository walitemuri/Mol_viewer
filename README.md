# Molecule Viewer: SDF Molecule Visualization Web Application

Author: Wali Temuri

## Description

MoleculeViewer is a powerful and efficient web application designed for scientists, researchers, and chemistry enthusiasts. It enables users to visualize and interact with molecular structures by parsing and rendering Structure Data File (SDF) formats with ease. The molecule information is processed and turned into an SVG object with aesthetic shading and colouring, to be viewed, rotated and you can change the colour of the atoms. 

### Parse and render SDF files that you Upload
![Mol_Viewer_MolDisplay](https://user-images.githubusercontent.com/108627530/233803138-4b0d4b8f-39f9-4d00-8923-e016b3569b10.gif)




### Delete and Add New Elements
![Mol_viewer_elementslist](https://user-images.githubusercontent.com/108627530/233803317-1e0abc44-7b5b-43b0-b38d-12bd1aa1b7e2.gif)



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

```bash
source setup.sh
```

This should compile the C program, now you must run the server with your desired port.
```
python3 ajaxserver.py {port_num}
```

## Preview -- Coming Soon

