import os, argparse, glob
import numpy as np, pandas as pd

ap = argparse.ArgumentParser(
    description="Analyze parity data from DIVE runs, binned by tetrahedron radius R (quantiles), and forecast sigma(pNL).",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument("-i", "--input", default=".", help="dir with the <set>_<real>_parity.txt files")
ap.add_argument("-b", "--nbins", type=int, default=20, help="number of R bins (quantiles)")
ap.add_argument("--nsample", type=int, default=5, help="nb of files used to set the bin edges")
ap.add_argument("--pNL", type=float, default=1e6, help="|pNL| injected in the ODD sims (P)")
args = ap.parse_args()

inputdir, NB, P = args.input, args.nbins, args.pNL
SETS = ["ODD_p", "ODD_m", "fiducial"]

def load(fname):                                   # fast read -> array (N, 2): R, parity
    return pd.read_csv(fname, sep=r"\s+", header=None).to_numpy()

n_real = len(glob.glob(f"{inputdir}/ODD_p_*_parity.txt"))   # realizations per set

# --- 1. quantile bin edges, from a few sample files ---
R_sample = np.concatenate([load(f"{inputdir}/fiducial_{r}_parity.txt")[:, 0]
                           for r in range(min(args.nsample, n_real))])
edges = np.percentile(R_sample, np.linspace(0, 100, NB + 1))
edges[0], edges[-1] = -np.inf, np.inf              # open outer bins -> catch everything
print("bin edges (Mpc/h):", np.round(edges, 2))

# --- 2. binned asymmetry for every simulation ---
A = {s: np.zeros((n_real, NB)) for s in SETS}      # A[s][real, bin] = N+ - N- in that bin

for s in SETS:
    for real in range(n_real):
        d = load(f"{inputdir}/{s}_{real}_parity.txt")
        R, sign = d[:, 0], np.sign(d[:, 1])
        b = np.digitize(R, edges)                  # bin index 1..NB for each tetrahedron
        for k in range(1, NB + 1):
            A[s][real, k - 1] = sign[b == k].sum()
        A[s][real] /= d.shape[0]          # normalize by the number of tetrahedra in that sim
    print(f"{s} done", flush=True)

# --- 3. save for the Fisher analysis later ---
np.save(f"{inputdir}/edges.npy", edges)
for s in SETS:
    np.save(f"{inputdir}/A_{s}_nb{NB}.npy", A[s])         # shape (n_real, NB)
print(f"saved edges.npy, A_<set>_nb{NB}.npy (n_real x nbins)")

# --- 4. Fisher forecast: sigma(pNL) ---
# response vector: alpha_k = <A_p - A_m> / (2P)   (paired-seed estimator)
alpha = (A["ODD_p"].mean(0) - A["ODD_m"].mean(0)) / (2 * P)     # (NB,)

# covariance from the fiducials only (the noise at pNL=0)
C = np.atleast_2d(np.cov(A["fiducial"], rowvar=False))          # (NB, NB), works for NB=1
Cinv = np.linalg.inv(C)

# Hartlap correction: unbiased inverse covariance (needs n_real >> NB)
hartlap = (n_real - NB - 2) / (n_real - 1)
Cinv *= hartlap
print(f"Hartlap factor = {hartlap:.3f}   (n_real={n_real}, nbins={NB})")

# Fisher scalar and constraint
F = alpha @ Cinv @ alpha
sigma_pNL = 1.0 / np.sqrt(F)
print(f"F = {F:.4e}")
print(f"sigma(pNL) = {sigma_pNL:.4e}   (1sigma error on pNL, one box volume)")

# sanity check: recover pNL by feeding the ODD_p mean as the observed vector
A_obs = A["ODD_p"].mean(0)
pNL_hat = (alpha @ Cinv @ A_obs) / F
print(f"check: pNL_hat(ODD_p mean) = {pNL_hat:.3e}   (should be ~+{P:.0e})")