# Project log — Delaunay-parity

## Monday, August 10

- **Project chosen:** parity violation in large-scale structure using Delaunay triangulation.
- **Set up the `delaunay-parity` repo** on my machine (with a `README` and a `.gitignore`), linked my SSH key to my GitHub account, then:
  `git init` → `git add .` → `git commit -m "message"` → `git branch -M main` → `git remote add origin git@github.com:josue-aubert/<repo-name>.git` → `git push -u origin main` (afterwards a plain `git push` is enough).
- **Forked Cheng's `DIVE` repo** to my GitHub, then cloned it locally with `git clone git@github.com:josue-aubert/DIVE.git`.
- **Created a conda environment `delaunay-parity`** and installed the requirements from `environment.yml`, which contains the compilation dependencies listed in the *Compilation* section of DIVE's README plus my own Python stack.
- **Compiled DIVE** and built the executable with: `cgal_create_CMakeLists -s DIVE` → `cmake -DCMAKE_BUILD_TYPE=Release .` → `make`.
- **Two separate repos** in the end: `delaunay-parity` (the analysis project) and `DIVE` (my modified fork of the C++ tool).
- **Created a toy test set** and checked that the whole chain runs correctly.

## Tuesday, August 11

We need a definition of parity on the 4 points (galaxies) of a tetrahedron such that: it flips sign under a parity transformation, it does not depend on the observer's position, and it is invariant under rotation → the **scalar triple product**.

**Definition (this work):**
- For each vertex, sum the (squared, for simplicity) lengths of its three edges, and use this to order the vertices in **increasing** order. `r0` is the vertex with the smallest edge-length sum, etc.
- Define `s_i = r_i - r_0`.
- The parity observable is the triple product `(s_1 × s_2) · s_3` (a pseudoscalar), equal to `det(s_1, s_2, s_3)`.

Inspired by *"Measurement of parity-odd modes in the large-scale 4-point correlation function of SDSS BOSS DR12 CMASS and LOWZ galaxies"*, J. Hou, Z. Slepian, R. N. Cahn — MNRAS 522, 5701 (2023), [arXiv:2206.03625](https://arxiv.org/abs/2206.03625). 

**Implementation:** coded this in `DIVE.cpp` (extra output column) and updated the README.

**Test (toy set):** for 500 random points in a box of side 1000, DIVE builds 3385 tetrahedra, of which **1680 have positive parity and 1705 negative**. The asymmetry is `A = N+ - N- = -25`. Under the null hypothesis of equiprobable signs, the standard deviation of `A` is `sqrt(N) = sqrt(3385) ≈ 58`, so the measurement is at `~0.4σ`, fully consistent with zero → the statistic is unbiased on parity-symmetric data.