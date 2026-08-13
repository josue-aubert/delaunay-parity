import os, argparse
import numpy as np, pandas as pd

ap = argparse.ArgumentParser(
    description="Analyze parity data from DIVE runs, binned by tetrahedron radius R (quantiles).",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument("-i", "--input", default=".", help="dir with the <set>_<real>_parity.txt files")
ap.add_argument("-b", "--nbins", type=int, default=20, help="number of R bins (quantiles)")
ap.add_argument("--nsample", type=int, default=5, help="nb of files used to set the bin edges")
args = ap.parse_args()

inputdir, NB = args.input, args.nbins
SETS = ["ODD_p", "ODD_m", "fiducial"]

def load(fname):                                   # fast read -> array (N, 2): R, parity
    return pd.read_csv(fname, sep=r"\s+", header=None).to_numpy()

n_real = len(os.listdir(inputdir)) // len(SETS)    # realizations per set

# --- 1. quantile bin edges, from a few sample files ---
R_sample = np.concatenate([load(f"{inputdir}/fiducial_{r}_parity.txt")[:, 0]
                           for r in range(min(args.nsample, n_real))])
edges = np.percentile(R_sample, np.linspace(0, 100, NB + 1))
edges[0], edges[-1] = -np.inf, np.inf              # open outer bins -> catch everything
print("bin edges (Mpc/h):", np.round(edges, 2))

# --- 2. binned asymmetry for every simulation ---
A = {s: np.zeros((n_real, NB)) for s in SETS}      # A[s][real, bin] = N+ - N- in that bin
T = {s: np.zeros(n_real) for s in SETS}            # total asymmetry per sim

for s in SETS:
    for real in range(n_real):
        d = load(f"{inputdir}/{s}_{real}_parity.txt")
        R, sign = d[:, 0], np.sign(d[:, 1])
        T[s][real] = sign.sum()
        b = np.digitize(R, edges)                  # bin index 1..NB for each tetrahedron
        for k in range(1, NB + 1):
            A[s][real, k - 1] = sign[b == k].sum()
        print(f"{s} {real}: T = {T[s][real]:.0f}", flush=True)

# --- 3. save for the Fisher analysis later ---
np.save(f"{inputdir}/edges.npy", edges)
for s in SETS:
    np.save(f"{inputdir}/A_{s}.npy", A[s])         # shape (n_real, NB)
    np.save(f"{inputdir}/T_{s}.npy", T[s])
print("saved edges.npy, A_<set>.npy (n_real x nbins), T_<set>.npy")