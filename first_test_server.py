#!/usr/bin/env python
import os, subprocess, argparse
import numpy as np, pandas as pd
import readfof

ap = argparse.ArgumentParser(
    description="Run DIVE on Quijote FoF catalogs; keep only (R, parity) per tetrahedron.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument("-i", "--input",  default=".",           help="dir with ODD_p/ ODD_m/ fiducial/")
ap.add_argument("-d", "--dive",   default="./DIVE",      help="path to the DIVE executable")
ap.add_argument("-o", "--output", default="./parity_out", help="output directory")
ap.add_argument("-n", "--num", type=int, default=None,   help="realizations per set (omit for all)")
args = ap.parse_args()

BASE, DIVE, OUT = args.input, args.dive, args.output
SNAP = {"ODD_p": 1, "ODD_m": 1, "fiducial": 4}
os.makedirs(OUT, exist_ok=True)

for s, snap in SNAP.items():
    setdir = f"{BASE}/{s}"
    reals = sorted([r for r in os.listdir(setdir) if os.path.isdir(f"{setdir}/{r}")], key=int)
    if args.num is not None:
        reals = reals[:args.num]
    for real in reals:
        FoF = readfof.FoF_catalog(f"{setdir}/{real}", snap, read_IDs=False)
        pos = FoF.GroupPos / 1e3
        tmp_pos  = f"{OUT}/pos_{s}_{real}.txt"
        tmp_full = f"{OUT}/full_{s}_{real}.txt"          # DIVE 5-col output (temp)
        np.savetxt(tmp_pos, pos, fmt="%.6f")
        subprocess.run([DIVE, "-i", tmp_pos, "-o", tmp_full, "-u", "1000"], check=True)
        # keep only column 3 (R) and column 4 (parity)
        Rp = pd.read_csv(tmp_full, sep=r"\s+", header=None, usecols=[3, 4]).to_numpy()
        out = f"{OUT}/{s}_{real}_parity.txt"
        np.savetxt(out, Rp, fmt="%.6g")                  # 2 columns: R  parity
        os.remove(tmp_pos)
        os.remove(tmp_full)
        print(f"{s} {real}: {len(pos)} halos -> {out}", flush=True)