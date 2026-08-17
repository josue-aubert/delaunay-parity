import os, subprocess, argparse
import numpy as np, pandas as pd
import readfof

ap = argparse.ArgumentParser(
    description="Run DIVE on a range of Quijote realizations; keep (R, chirality, chirality_shape) per tetrahedron.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument("-i", "--input",  default=".",            help="dir with ODD_p/ ODD_m/ fiducial/")
ap.add_argument("-d", "--dive",   default="./DIVE",       help="path to the DIVE executable")
ap.add_argument("-o", "--output", default="./parity_out", help="output directory")
ap.add_argument("-s", "--start", type=int, default=0,   help="first realization (inclusive)")
ap.add_argument("-e", "--end",   type=int, default=500, help="last realization (exclusive)")
ap.add_argument("--mmin", type=float, default=0.0, help="minimum halo mass in Msun/h (0 = no cut)")
args = ap.parse_args()

BASE, DIVE, OUT, MMIN = args.input, args.dive, args.output, args.mmin
SNAP = {"ODD_p": 1, "ODD_m": 1, "fiducial": 4}
os.makedirs(OUT, exist_ok=True)

for s, snap in SNAP.items():
    for real in range(args.start, args.end):
        snapdir = f"{BASE}/{s}/{real}"
        if not os.path.isdir(snapdir):
            continue
        FoF  = readfof.FoF_catalog(snapdir, snap, read_IDs=False)
        pos  = FoF.GroupPos / 1e3               # Mpc/h
        mass = FoF.GroupMass * 1e10             # Msun/h

        if MMIN > 0:                            # same cut for ALL sets
            sel = mass >= MMIN
            pos = pos[sel]

        tmp_pos  = f"{OUT}/pos_{s}_{real}.txt"
        tmp_full = f"{OUT}/full_{s}_{real}.txt"
        np.savetxt(tmp_pos, pos, fmt="%.6f")
        subprocess.run([DIVE, "-i", tmp_pos, "-o", tmp_full, "-u", "1000"], check=True)
        Rp = pd.read_csv(tmp_full, sep=r"\s+", header=None, usecols=[3, 4, 5]).to_numpy()
        out = f"{OUT}/{s}_{real}_parity.txt"
        np.savetxt(out, Rp, fmt="%.6g")
        os.remove(tmp_pos); os.remove(tmp_full)
        print(f"{s} {real}: {len(pos)} halos -> {out}", flush=True)