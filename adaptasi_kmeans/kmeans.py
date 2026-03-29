import subprocess
import math

MAX_ITERATIONS = 5
CONVERGENCE_THRESHOLD = 0.001
csv_file = "games.csv"

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
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)

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


print(f"File CSV    : {csv_file}")
print(f"K           : 11 cluster")
print(f"Max iterasi : {MAX_ITERATIONS}")
print(f"Threshold   : {CONVERGENCE_THRESHOLD}")

current_file = "centroids_0.txt"

for iteration in range(1, MAX_ITERATIONS + 1):
    old = load_centroids(current_file)
    print(f"\nIterasi {iteration}")

    new = run_iteration(current_file, csv_file, iteration)

    new_file = f"centroids_{iteration}.txt"
    save_centroids(new_file, new)
    current_file = new_file

    shift = centroid_shift(old, new)
    print(f"  Max centroid shift: {shift:.6f}")

    if shift < CONVERGENCE_THRESHOLD:
        print(f"Konvergen di iterasi {iteration}")
        break
else:
    print(f"\nSelesai (max iterasi {MAX_ITERATIONS} tercapai)")

# Hasil akhir
final = load_centroids(current_file)
print(f"\nHasil: {len(final)} cluster ditemukan")
print(f"File centroid akhir: {current_file}")