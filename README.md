# delaunay-parity

Looking for parity violation in the large-scale structure using the Delaunay triangulation of galaxies. Idea: for each Delaunay tetrahedron, compute a chirality (signed volume) that flips under a parity transformation, and look for an imbalance between left- and right-handed tetrahedra (a parity-odd signal would point to new physics in the initial conditions).

This is a cheaper alternative to the usual 4-point correlation function. Now being tested on the Quijote-ODD simulations.

Triangulation done with a modified fork of DIVE; analysis in Python here.

Research visit @ Tsinghua (Prof. Cheng Zhao).