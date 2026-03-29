#!/usr/bin/env python3
"""
mapper_csv.py — Mapper KMeans untuk CSV Steam

Kolom yang dipakai (semua numerik):
  Peak CCU, Required age, Price, DiscountDLC count,
  Positive, Negative, Score rank, Average playtime two weeks,
  Median playtime forever, Median playtime two weeks, Recommendations

Jalankan:
  python mapper_csv.py centroids_0.txt < data.csv
"""

import sys
import math
import csv

# --- Kolom numerik yang akan digunakan ---
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
    """Baca centroid. Format: cluster_id,v0,v1,...,v10"""
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
    try:
        with open(filepath) as f:
            reader = csv.DictReader(f)
            for row in reader:
                col = row["col"]
                stats[col] = {
                    "mean": float(row["mean"]),
                    "std":  float(row["std"]),
                }
    except FileNotFoundError:
        # Jika belum ada stats, gunakan raw value (tanpa normalisasi)
        pass
    return stats

def parse_row(row, col_stats):
    """
    Ambil nilai 11 kolom numerik dari satu baris CSV.
    Return list of float, atau None jika ada kolom kosong/invalid.
    """
    vector = []
    for col in NUMERIC_COLS:
        raw = row.get(col, "").strip()
        if raw == "" or raw is None:
            return None  # skip baris yang ada kolom kosong
        try:
            val = float(raw)
        except ValueError:
            return None
        # Normalisasi jika stats tersedia
        if col_stats and col in col_stats:
            val = normalize(val, col_stats, col)
        vector.append(val)
    return vector

def mapper(centroid_file):
    centroids = load_centroids(centroid_file)
    col_stats  = load_col_stats("col_stats.csv")

    reader = csv.DictReader(sys.stdin)
    skipped = 0
    processed = 0

    for row in reader:
        vector = parse_row(row, col_stats)
        if vector is None:
            skipped += 1
            continue

        # Hitung jarak ke semua centroid
        distances = [
            (cid, euclidean(vector, centroid))
            for cid, centroid in centroids
        ]
        nearest_cid = min(distances, key=lambda d: d[1])[0]

        # EMIT: "cluster_id\tv0,v1,...,v10"
        vec_str = ",".join(f"{v:.6f}" for v in vector)
        print(f"{nearest_cid}\t{vec_str}")
        processed += 1

    print(f"[mapper] processed={processed} skipped={skipped}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mapper_csv.py <centroid_file>", file=sys.stderr)
        sys.exit(1)
    mapper(sys.argv[1])