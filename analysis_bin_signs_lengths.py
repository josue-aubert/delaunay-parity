import os, argparse, glob
import numpy as np, matplotlib.pyplot as plt

ap = argparse.ArgumentParser(
    description="Per-bin paired SNR of the signs statistic, binned by edge-length ratios.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument("-i", "--input", default=".", help="dir with the <set>_<real>_parity.npy files")
ap.add_argument("-b", "--nbins", type=int, default=20, help="number of quantile bins per ratio")
ap.add_argument("--nsample", type=int, default=5, help="nb of files used to set the bin edges")
args = ap.parse_args()

inputdir, NB = args.input, args.nbins
SETS = ["ODD_p", "ODD_m", "fiducial"]

# ratio definitions: (label, numerator column, denominator column)   [col0=chirality, col1=l1, col2=l2, col3=l3]
RATIOS = [("l1/l2", 1, 2), ("l1/l3", 1, 3), ("l2/l3", 2, 3)]
SINGLE = [0, 1, 2]                       # one-ratio configs -> line plots
PAIRS  = [(0, 1), (0, 2), (1, 2)]        # two-ratio configs -> heatmaps

def load(fname):
    return np.load(fname)

def ratio(d, i):
    _, cn, cd = RATIOS[i]
    return d[:, cn] / d[:, cd]

n_real = len(glob.glob(f"{inputdir}/ODD_p_*_parity.npy"))   # realizations per set

# --- 1. quantile edges + bin centers for each of the 3 ratios (from sample fiducials) ---
edges, centers = [], []
for i in range(3):
    samp = np.concatenate([ratio(load(f"{inputdir}/fiducial_{r}_parity.npy"), i)
                           for r in range(min(args.nsample, n_real))])
    e = np.percentile(samp, np.linspace(0, 100, NB + 1))
    e[0], e[-1] = -np.inf, np.inf                 # open outer bins -> catch everything
    fin = e.copy()
    fin[0]  = fin[1]  - (fin[2]  - fin[1])         # finite extrapolation for the centers
    fin[-1] = fin[-2] + (fin[-2] - fin[-3])
    edges.append(e)
    centers.append(0.5 * (fin[:-1] + fin[1:]))

# --- 2. single pass over all sims: fill the 6 configurations ---
A1 = {i: {s: np.zeros((n_real, NB))      for s in SETS} for i in SINGLE}   # (n_real, NB)
A2 = {p: {s: np.zeros((n_real, NB * NB)) for s in SETS} for p in PAIRS}    # (n_real, NB*NB)

for s in SETS:
    for real in range(n_real):
        d = load(f"{inputdir}/{s}_{real}_parity.npy")
        sign = np.sign(d[:, 0])                    # sign of the chirality
        Ntet = d.shape[0]
        b = [np.digitize(ratio(d, i), edges[i]) - 1 for i in range(3)]   # bin index (0..NB-1) per ratio
        for i in SINGLE:                           # 1D bins
            A1[i][s][real] = np.bincount(b[i], weights=sign, minlength=NB)[:NB] / Ntet
        for (i, j) in PAIRS:                       # 2D bins (flattened)
            flat = b[i] * NB + b[j]
            A2[(i, j)][s][real] = np.bincount(flat, weights=sign, minlength=NB * NB)[:NB * NB] / Ntet
        print(f"{s}, {real} done", flush=True)

# --- 3. paired SNR helper (cosmic variance cancelled) ---
def paired_snr(A):
    D = A["ODD_p"] - A["ODD_m"]                    # (n_real, ...)
    mean_D = D.mean(0)
    err_D  = D.std(0, ddof=1) / np.sqrt(n_real)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(err_D > 0, mean_D / err_D, 0.0)

# --- 4. the 3 line plots (one ratio each) ---
for i in SINGLE:
    snr = paired_snr(A1[i])
    lab = RATIOS[i][0]
    plt.figure(figsize=(7, 4.5))
    plt.axhline(0, color="k", lw=0.8, ls="--")
    plt.plot(centers[i], snr, "o-", color="C3", lw=1.3, ms=5)
    plt.xlabel(f"Edge-length ratio {lab}")
    plt.ylabel(r"SNR $= \langle A_+ - A_-\rangle / \sigma$")
    plt.title(f"Per-bin paired SNR — signs, binned by {lab}  ({NB} bins)")
    plt.tight_layout()
    name = f"SNR_signs_{lab.replace('/', '')}_nb{NB}.png"
    plt.savefig(name, dpi=150); plt.close()
    print("saved", name)

# --- 5. the 3 heatmaps (pair of ratios each) ---
for (i, j) in PAIRS:
    snr = paired_snr(A2[(i, j)]).reshape(NB, NB)   # snr[bin_i, bin_j]
    li, lj = RATIOS[i][0], RATIOS[j][0]
    vmax = np.max(np.abs(snr)) or 1.0              # symmetric color scale around 0
    plt.figure(figsize=(6.4, 5))
    im = plt.pcolormesh(centers[i], centers[j], snr.T, cmap="RdBu_r",
                        vmin=-vmax, vmax=vmax, shading="auto")
    plt.colorbar(im, label=r"SNR $= \langle A_+ - A_-\rangle / \sigma$")
    plt.xlabel(f"Edge-length ratio {li}")
    plt.ylabel(f"Edge-length ratio {lj}")
    plt.title(f"Per-cell paired SNR — signs, binned by ({li}, {lj})  ({NB}x{NB})")
    plt.tight_layout()
    name = f"SNR_signs_{li.replace('/', '')}_{lj.replace('/', '')}_nb{NB}.png"
    plt.savefig(name, dpi=150); plt.close()
    print("saved", name)