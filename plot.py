import argparse, glob
import numpy as np, matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", default=".")
ap.add_argument("-b", "--nbins", type=int, default=20)
ap.add_argument("-m", "--method", default="shapes", choices=["signs", "shapes"])
args = ap.parse_args()
inputdir, NB, method = args.input, args.nbins, args.method  

SETS   = ["ODD_p", "ODD_m", "fiducial"]
LABELS = {"ODD_p": r"$p_{\rm NL}=+10^6$", "ODD_m": r"$p_{\rm NL}=-10^6$", "fiducial": r"$p_{\rm NL}=0$"}
COLORS = {"ODD_p": "C3", "ODD_m": "C0", "fiducial": "0.4"}

# --- bin centers in R (from the saved quantile edges; fix the +/-inf ends) ---
edges = np.load(f"{inputdir}/edges_{method}_nb{NB}.npy").astype(float)
fin = edges.copy()
fin[0]  = fin[1]  - (fin[2]  - fin[1])       # extrapolate the open outer bins
fin[-1] = fin[-2] + (fin[-2] - fin[-3])
centers = 0.5 * (fin[:-1] + fin[1:])

# --- plot A(R) for the three cosmologies ---
plt.figure(figsize=(7, 4.5))
for s in SETS:
    A = np.load(f"{inputdir}/A_{method}_{s}_nb{NB}.npy")          # (n_real, NB)
    mean = A.mean(0)
    err  = A.std(0) / np.sqrt(A.shape[0])                # error on the mean
    plt.errorbar(centers, mean, yerr=err, label=LABELS[s],
                 color=COLORS[s], marker="o", ms=4, capsize=2, lw=1.3)
    
if method == "shapes":
    plt.axhline(0, color="k", lw=0.8, ls="--")
    plt.xlabel(r"Circumsphere radius  $R$  [Mpc/$h$]")
    plt.ylabel(r"$Sum(A)/N_{\rm tet}$  per bin")
    plt.title(f" Summed chirality shapes bins vs scale  ({NB} R-bins)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"./A_of_R_{method}_nb{NB}.png", dpi=150)
    plt.show()
    print(f"saved A_of_R_{method}_nb{NB}.png")
    
if method == "signs":
    plt.axhline(0, color="k", lw=0.8, ls="--")
    plt.xlabel(r"Circumsphere radius  $R$  [Mpc/$h$]")
    plt.ylabel(r"$(N_+ - N_-)/N_{\rm tet}$  per bin")
    plt.title(f"Summed parity signs over bins vs scale  ({NB} R-bins)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"./A_of_R_{method}_nb{NB}.png", dpi=150)
    plt.show()
    print(f"saved A_of_R_{method}_nb{NB}.png")

