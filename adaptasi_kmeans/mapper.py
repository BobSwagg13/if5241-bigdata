import sys
import math
import csv

# baca CSV dari stdin dengan field numerik yang akan dipakai untuk clustering

NUMERIC_COLS = [
    "Peak CCU",
    "Required age",
    "Price",
    "DiscountDLC count",
    "Positive",
    "Negative",
    "Score rank",
    "Average playtime two weeks",
    "Median playtime forever",
    "Median playtime two weeks",
    "Recommendations",
]

def euclidean(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))

def load_centroids(filepath):
    "Baca centroid. Format: cluster_id,v0,v1,...,v10"
    centroids = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            cid = int(parts[0])
            vector = [float(x) for x in parts[1:]]
            centroids.append((cid, vector))
    return centroids

def normalize(value, col_stats, col_name):
    """
    Z-score normalization agar kolom dengan skala besar
    (misal Positive bisa jutaan) tidak mendominasi jarak.
    Pakai mean dan std dari col_stats.
    """
    mean = col_stats[col_name]["mean"]
    std  = col_stats[col_name]["std"]
    if std == 0:
        return 0.0
    return (value - mean) / std

def load_col_stats(filepath="col_stats.csv"):
    """Baca statistik kolom (mean, std) yang dihitung oleh preprocess.py"""
    stats = {}
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            col = row["col"]
            stats[col] = {
                "mean": float(row["mean"]),
                "std":  float(row["std"]),
            }
    return stats

def parse_row(row, col_stats):
    """
    Ambil nilai 11 kolom numerik dari satu baris CSV.
    """
    vector = []
    for col in NUMERIC_COLS:
        raw = row[col].strip()
        val = float(raw)
        val = normalize(val, col_stats, col)
        vector.append(val)
    return vector

def mapper(centroid_file):
    centroids = load_centroids(centroid_file)
    col_stats  = load_col_stats("col_stats.csv")

    reader = csv.DictReader(sys.stdin)
    processed = 0

    for row in reader:
        vector = parse_row(row, col_stats)

        # cari centroid terdekat untuk vektor ini
        distances = [
            (cid, euclidean(vector, centroid))
            for cid, centroid in centroids
        ]
        nearest_cid = min(distances, key=lambda d: d[1])[0]

        # EMIT: "cluster_id\tv0,v1,...,v10"
        vec_str = ",".join(f"{v:.6f}" for v in vector)
        print(f"{nearest_cid}\t{vec_str}")
        processed += 1

centroid_file = sys.argv[1]
mapper(centroid_file)