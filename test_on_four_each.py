import os, subprocess
import numpy as np
import readfof

BASE = "/Users/josueaubert/Documents/Tsinghua2026/delaunay-parity"
DIVE = "/Users/josueaubert/Documents/Tsinghua2026/DIVE/DIVE"
OUT  = "/Users/josueaubert/Documents/Tsinghua2026/delaunay-parity/test_on_four_each_out"
SNAP = {"ODD_p": 1, "ODD_m": 1, "fiducial": 4}

os.makedirs(OUT, exist_ok=True)

for s, snap in SNAP.items():
    setdir = f"{BASE}/{s}"
    for real in sorted(os.listdir(setdir)):
        snapdir = f"{setdir}/{real}"
        if not os.path.isdir(snapdir):
            continue
        FoF = readfof.FoF_catalog(snapdir, snap, read_IDs=False)
        pos = FoF.GroupPos / 1e3
        tmp = f"{OUT}/pos_{s}_{real}.txt"
        np.savetxt(tmp, pos, fmt="%.6f")
        out = f"{OUT}/{s}_{real}_parity.txt"
        subprocess.run([DIVE, "-i", tmp, "-o", out, "-u", "1000"], check=True)
        os.remove(tmp)
        print(f"{s} {real}: {len(pos)} halos -> {out}", flush=True)