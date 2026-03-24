import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split("\t")

    product = fields[3]
    price = fields[4]

    price = float(price)

    if "Toys" in product:
        print(f"Toys\t{price}")

    if "Consumer Electronics" in product:
        print(f"Consumer Electronics\t{price}")