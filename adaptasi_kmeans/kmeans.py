#!/usr/bin/env python3
"""
run_kmeans_csv.py — Loop iterasi KMeans untuk CSV Steam

Urutan penggunaan:
  1. python preprocess_csv.py data_steam.csv   ← wajib dulu
  2. python run_kmeans_csv.py data_steam.csv   ← ini

Cara kerja tiap iterasi:
  mapper_csv.py | sort | reducer_csv.py
"""

import subprocess
import sys
import os
import math

MAX_ITERATIONS = 5
CONVERGENCE_THRESHOLD = 0.001

def load_centroids(filepath):
    centroids = {}
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            cid = int(parts[0])
            centroids[cid] = [float(x) for x in parts[1:]]
    return centroids

def save_centroids(filepath, centroids):
    with open(filepath, "w") as f:
        for cid in sorted(centroids.keys()):
            vec_str = ",".join(f"{v:.6f}" for v in centroids[cid])
            f.write(f"{cid},{vec_str}\n")

def centroid_shift(old, new):
    """Jarak maksimum yang bergerak di antara semua centroid."""
    max_shift = 0.0
    for cid in old:
        if cid not in new:
            continue
        dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(old[cid], new[cid])))
        max_shift = max(max_shift, dist)
    return max_shift

def run_iteration(centroid_file, csv_file, iteration):
    cmd = (
        f"python3 mapper.py {centroid_file} < {csv_file}"
        f" | sort"
        f" | python3 reducer.py"
    )
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[ERROR] Iterasi {iteration} gagal!")
        print(result.stderr)
        return None

    new_centroids = {}
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split(",")
        cid = int(parts[0])
        new_centroids[cid] = [float(x) for x in parts[1:]]

    # Tampilkan log dari mapper/reducer
    for line in result.stderr.strip().split("\n"):
        if line:
            print("  " + line)

    return new_centroids

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_kmeans_csv.py <file.csv>")
        print("Pastikan sudah jalankan: python preprocess_csv.py <file.csv>")
        sys.exit(1)

    csv_file = sys.argv[1]

    if not os.path.exists("centroids_0.txt"):
        print("[ERROR] centroids_0.txt tidak ditemukan.")
        print("        Jalankan dulu: python preprocess_csv.py", csv_file)
        sys.exit(1)

    if not os.path.exists("games.csv"):
        print("[ERROR] games.csv tidak ditemukan.")
        print("        Jalankan dulu: python preprocess_csv.py", csv_file)
        sys.exit(1)

    print("=" * 55)
    print("KMeans MapReduce — Steam CSV")
    print("=" * 55)
    print(f"File CSV    : {csv_file}")
    print(f"K           : 11 cluster")
    print(f"Max iterasi : {MAX_ITERATIONS}")
    print(f"Threshold   : {CONVERGENCE_THRESHOLD}")

    current_file = "centroids_0.txt"

    for iteration in range(1, MAX_ITERATIONS + 1):
        old = load_centroids(current_file)
        print(f"\n--- Iterasi {iteration} ---")

        new = run_iteration(current_file, csv_file, iteration)
        if new is None:
            break

        new_file = f"centroids_{iteration}.txt"
        save_centroids(new_file, new)
        current_file = new_file

        shift = centroid_shift(old, new)
        print(f"  Max centroid shift: {shift:.6f}")

        if shift < CONVERGENCE_THRESHOLD:
            print(f"\n{'='*55}")
            print(f"Konvergen di iterasi {iteration}! (shift={shift:.6f})")
            print(f"{'='*55}")
            break
    else:
        print(f"\nSelesai (max iterasi {MAX_ITERATIONS} tercapai)")

    # Hasil akhir
    final = load_centroids(current_file)
    print(f"\nHasil: {len(final)} cluster ditemukan")
    print(f"File centroid akhir: {current_file}")
    print("\nSelesai.")

if __name__ == "__main__":
    main()