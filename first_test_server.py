#!/usr/bin/env python
import os, subprocess, argparse
import numpy as np
import readfof

ap = argparse.ArgumentParser(
    description="Apply DIVE to Quijote FoF halo catalogs and output a file text for each with 5 columns : x y z position of the center of the circons sphere, radius of the sphere and parity.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument("-i", "--input",  default=".",
                help="input directory containing the ODD_p/ ODD_m/ fiducial/ folders")
ap.add_argument("-d", "--dive",   default="./DIVE",
                help="path to the compiled DIVE executable")
ap.add_argument("-o", "--output", default="./parity_out",
                help="output directory for the parity catalogs")
ap.add_argument("-n", "--num", type=int, default=None,
                help="number of realizations considered, ordered by name (omit for all)")
args = ap.parse_args()

BASE, DIVE, OUT = args.input, args.dive, args.output
SNAP = {"ODD_p": 1, "ODD_m": 1, "fiducial": 4}   # snapnum for z=0
os.makedirs(OUT, exist_ok=True)

for s, snap in SNAP.items():
    setdir = f"{BASE}/{s}"
    reals = [r for r in os.listdir(setdir) if os.path.isdir(f"{setdir}/{r}")]
    reals = sorted(reals, key=int)               # numeric order: 0,1,2,...,10,11
    if args.num is not None:
        reals = reals[:args.num]                 # keep only the first N
    for real in reals:
        snapdir = f"{setdir}/{real}"
        FoF = readfof.FoF_catalog(snapdir, snap, read_IDs=False)
        pos = FoF.GroupPos / 1e3
        tmp = f"{OUT}/pos_{s}_{real}.txt"
        np.savetxt(tmp, pos, fmt="%.6f")
        out = f"{OUT}/{s}_{real}_parity.txt"
        subprocess.run([DIVE, "-i", tmp, "-o", out, "-u", "1000"], check=True)
        os.remove(tmp)
        print(f"{s} {real}: {len(pos)} halos -> {out}", flush=True)