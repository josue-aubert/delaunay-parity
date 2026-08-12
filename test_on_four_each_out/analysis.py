import numpy as np
import matplotlib.pyplot as plt

datadir = "/Users/josueaubert/Documents/Tsinghua2026/delaunay-parity/test_on_four_each_out"

Ts_ODD_p = []
Ts_ODD_m = []
Ts_fiducial = []

for s in ["ODD_p", "ODD_m", "fiducial"]:
    for real in range(0, 4):
        filename = f"{datadir}/{s}_{real}_parity.txt"
        parity = np.loadtxt(filename, usecols=4)
        parity_signs = np.sign(parity)
        T = parity_signs.sum()
        print(f"{s} {real}: T = {T}, Number of sim = {len(parity_signs)}")
        if s == "ODD_p":
            Ts_ODD_p.append(T)
        elif s == "ODD_m":
            Ts_ODD_m.append(T)
        else:
            Ts_fiducial.append(T)
            
ODD_p_mean = np.mean(Ts_ODD_p)
ODD_m_mean = np.mean(Ts_ODD_m)
fiducial_mean = np.mean(Ts_fiducial)
ODD_p_std = np.std(Ts_ODD_p)
ODD_m_std = np.std(Ts_ODD_m)
fiducial_std = np.std(Ts_fiducial)
print(f"ODD_p mean T = {ODD_p_mean}, std = {ODD_p_std}")
print(f"ODD_m mean T = {ODD_m_mean}, std = {ODD_m_std}")
print(f"fiducial mean T = {fiducial_mean}, std = {fiducial_std}")

