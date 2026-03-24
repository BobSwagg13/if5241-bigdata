import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split("\t")

    city = fields[2]
    product = fields[3]
    price = fields[4]

    price = float(price)

    if city in ("Miami", "San Francisco", "Atlanta"):
        print(f"{city}\t{price}\t{product}")
