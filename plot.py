import argparse
import numpy as np, matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", default=".")
ap.add_argument("-b", "--nbins", type=int, default=20)
ap.add_argument("-m", "--method", default="shapes", choices=["signs", "shapes"])
args = ap.parse_args()
inputdir, NB, method = args.input, args.nbins, args.method

LABEL = {"signs":  r"$(N_+ - N_-)/N_{\rm tet}$",
         "shapes": r"$\sum \hat\chi / N_{\rm tet}$"}[method]

# --- bin centers in R (from the saved quantile edges; fix the +/-inf ends) ---
edges = np.load(f"{inputdir}/edges_{method}_nb{NB}.npy").astype(float)
fin = edges.copy()
fin[0]  = fin[1]  - (fin[2]  - fin[1])       # extrapolate the open outer bins
fin[-1] = fin[-2] + (fin[-2] - fin[-3])
centers = 0.5 * (fin[:-1] + fin[1:])

# --- paired per-bin SNR: (A_+ - A_-) / error-on-the-mean, cosmic variance cancelled ---
A_p = np.load(f"{inputdir}/A_{method}_ODD_p_nb{NB}.npy")     # (n_real, NB)
A_m = np.load(f"{inputdir}/A_{method}_ODD_m_nb{NB}.npy")     # (n_real, NB)
n_real = A_p.shape[0]

D      = A_p - A_m                            # paired difference, per seed
mean_D = D.mean(0)                            # mean over the sims, per bin
err_D  = D.std(0, ddof=1) / np.sqrt(n_real)   # error on the mean, per bin
snr    = mean_D / err_D                       # SNR in each bin

# --- plot ---
plt.figure(figsize=(7, 4.5))
plt.axhline(1, color="k", lw=0.8, ls="--")
plt.axhline(-1, color="k", lw=0.8, ls="--")
plt.plot(centers, snr, "o-", color="C3", lw=1.3, ms=5)
plt.xlabel(r"Circumsphere radius  $R$  [Mpc/$h$]")
plt.ylabel(r"SNR $= \langle A_+ - A_- \rangle \, / \, \sigma$")
plt.title(f"Per-bin paired SNR — {method} statistic ({NB} R-bins)")
plt.tight_layout()
plt.savefig(f"./SNR_of_R_{method}_nb{NB}.png", dpi=150)
print(f"saved SNR_of_R_{method}_nb{NB}.png")