import csv
import random
import math

K = 11

NUMERIC_COLS = [
    "Peak CCU", "Required age", "Price", "DiscountDLC count",
    "Positive", "Negative", "Score rank",
    "Average playtime two weeks", "Median playtime forever",
    "Median playtime two weeks", "Recommendations",
]

csv_file = "games.csv"

# Kumpulkan semua vector valid (untuk stats & sampling) 
all_vectors = []

with open(csv_file, encoding="utf-8", errors="replace") as f:
    reader = csv.DictReader(f)

    for row in reader:
        vec = [float(row[col].strip()) for col in NUMERIC_COLS]
        all_vectors.append(vec)

# --- Hitung mean & std tiap kolom ---
n = len(all_vectors)
dims = len(NUMERIC_COLS)

means = [sum(v[d] for v in all_vectors) / n for d in range(dims)]
stds  = [
    math.sqrt(sum((v[d] - means[d]) ** 2 for v in all_vectors) / n)
    for d in range(dims)
]

with open("col_stats.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["col", "mean", "std"])
    for i, col in enumerate(NUMERIC_COLS):
        writer.writerow([col, f"{means[i]:.6f}", f"{stds[i]:.6f}"])
        print(f"    {col:35s} mean={means[i]:12.2f}  std={stds[i]:12.2f}")

#Inisialisasi centroid dengan pilih acak
# Normalisasi dulu untuk sampling yang lebih baik
def normalize_vec(vec):
    return [
        (vec[d] - means[d]) / stds[d] if stds[d] > 0 else 0.0
        for d in range(dims)
    ]

sample_indices = random.sample(range(len(all_vectors)), K)
init_centroids = [normalize_vec(all_vectors[i]) for i in sample_indices]

with open("centroids_0.txt", "w") as f:
    for cid, vec in enumerate(init_centroids):
        vec_str = ",".join(f"{v:.6f}" for v in vec)
        f.write(f"{cid},{vec_str}\n")
