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
        parts = line.split("\t")
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

reducer()