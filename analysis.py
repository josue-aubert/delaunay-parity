import os, argparse
import numpy as np, pandas as pd

ap = argparse.ArgumentParser(
    description="Analyze parity data from DIVE runs.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ap.add_argument("-i", "--input",  default=".",
                help="input directory containing ONLY the ODD_p/ ODD_m/ fiducial/ folders")
args = ap.parse_args()

inputdir = args.input

Ts_ODD_p = []
Ts_ODD_m = []
Ts_fiducial = []
As_ODD_p = []
As_ODD_m = []
As_fiducial = []

n_realizations = len(os.listdir(inputdir)) // 3    # Assuming equal number of realizations for each set

for s in ["ODD_p", "ODD_m", "fiducial"]:
    for real in range(0, n_realizations):
        filename = f"{inputdir}/{s}_{real}_parity.txt"
        parity = pd.read_csv(filename, sep=r"\s+", header=None, usecols=[1]).to_numpy().ravel()/1000.0
        parity_signs = np.sign(parity)
        A = parity_signs.sum()
        T = parity.sum()
        print(f"{s} {real}: A = {A}, T = {T}, Number of tetrahedra = {len(parity_signs)}")
        if s == "ODD_p":
            As_ODD_p.append(A)
            Ts_ODD_p.append(T)
        elif s == "ODD_m":
            As_ODD_m.append(A)
            Ts_ODD_m.append(T)
        else:
            As_fiducial.append(A)
            Ts_fiducial.append(T)

ODD_p_A_mean = np.mean(As_ODD_p)
ODD_m_A_mean = np.mean(As_ODD_m)
fiducial_A_mean = np.mean(As_fiducial)
ODD_p_A_std = np.std(As_ODD_p)
ODD_m_A_std = np.std(As_ODD_m)
fiducial_A_std = np.std(As_fiducial)

ODD_p_T_mean = np.mean(Ts_ODD_p)
ODD_m_T_mean = np.mean(Ts_ODD_m)
fiducial_T_mean = np.mean(Ts_fiducial)
ODD_p_T_std = np.std(Ts_ODD_p)
ODD_m_T_std = np.std(Ts_ODD_m)
fiducial_T_std = np.std(Ts_fiducial)

print(f"ODD_p mean A = {ODD_p_A_mean}, std = {ODD_p_A_std}")
print(f"ODD_m mean A = {ODD_m_A_mean}, std = {ODD_m_A_std}")
print(f"fiducial mean A = {fiducial_A_mean}, std = {fiducial_A_std}")
print(f"ODD_p mean T = {ODD_p_T_mean}, std = {ODD_p_T_std}")
print(f"ODD_m mean T = {ODD_m_T_mean}, std = {ODD_m_T_std}")
print(f"fiducial mean T = {fiducial_T_mean}, std = {fiducial_T_std}")