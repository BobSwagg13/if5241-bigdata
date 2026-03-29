#!/usr/bin/env python3
"""
reducer_csv.py — Reducer KMeans untuk CSV Steam (11 kolom)

Input dari mapper_csv.py: "cluster_id\tv0,v1,...,v10"
Output: "cluster_id,new_v0,new_v1,...,new_v10"  ← centroid baru

Jalankan (pipeline):
  python mapper_csv.py centroids_0.txt < data.csv | sort | python reducer_csv.py
"""

import sys
from collections import defaultdict

NUMERIC_COLS = [
    "Peak CCU", "Required age", "Price", "DiscountDLC count",
    "Positive", "Negative", "Score rank",
    "Average playtime two weeks", "Median playtime forever",
    "Median playtime two weeks", "Recommendations",
]

def reducer():
    clusters = defaultdict(list)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) != 2:
            continue

        cid = int(parts[0])
        vector = [float(x) for x in parts[1].split(",")]
        clusters[cid].append(vector)

    for cid in sorted(clusters.keys()):
        points = clusters[cid]
        n = len(points)
        dims = len(points[0])

        # Mean tiap dimensi
        new_centroid = [
            sum(p[d] for p in points) / n
            for d in range(dims)
        ]

        # EMIT centroid baru
        vec_str = ",".join(f"{v:.6f}" for v in new_centroid)
        print(f"{cid},{vec_str}")

        # Log ke stderr
        print(f"  Cluster {cid}: {n} titik", file=sys.stderr)

if __name__ == "__main__":
    reducer()