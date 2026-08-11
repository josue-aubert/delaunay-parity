import numpy as np

rng = np.random.default_rng(seed=42)

L = 1000.0
points = rng.uniform(0.0, L, size=(500, 3))

np.savetxt("toy.txt", points, fmt="%.6f")

print(f"{len(points)} points écrits dans toy.txt")