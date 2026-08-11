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

### First run on Quijote

**Simulations (from the Quijote table).** Matched sets, all *standard / 2LPT / 512³*:
- `ODD_p`: pNL = +1e6, 500 realizations
- `ODD_m`: pNL = -1e6, 500 realizations
- `fiducial`: pNL = 0, 15,000 realizations (the first 500 share seeds with ODD)

**Data.** Downloaded one FoF halo catalog of each via Globus, at z=0. Watch the
redshift/snapshot mapping, it differs for ODD:
- fiducial: `/Halos/FoF/fiducial/10825/groups_004/` (snapnum 4 → z=0)
- ODD_p: `/Halos/FoF/ODD_p/310/groups_001/` (snapnum 1 → z=0 for ODD)
- ODD_m: `/Halos/FoF/ODD_m/310/groups_001/` (snapnum 1 → z=0 for ODD)

Read with Pylians' `readfof` (needs the structure `basedir/groups_XXX/group_tab_XXX.*`;
it stitches the sub-files automatically), extracted halo positions
`GroupPos/1e3` (Mpc/h) and saved them as `x y z` text files for DIVE.

**Results** (~4×10⁵ halos each, no mass cut for the moment):

| simulation | pNL   | N_tet    | asymmetry A | A/√N   |
|------------|-------|----------|-------------|--------|
| fiducial   | 0     | 2757091  | -1785       | -1.1σ  |
| ODD_p      | +1e6  | 2751143  | +1329       | +0.8σ  |
| ODD_m      | -1e6  | 2752269  | +303        | +0.2σ  |

- **Null test passes** on the real fiducial: A = -1785 ≈ -1.1σ, consistent with zero.
- **Paired difference:** A(ODD_p) - A(ODD_m) = 1329 - 303 = **+1026**, with the
  expected sign (pNL>0 gives a more positive asymmetry).