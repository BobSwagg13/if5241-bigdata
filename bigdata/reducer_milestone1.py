import sys

current_category = None
current_total = 0.0

for line in sys.stdin:
    line = line.strip()
    parts = line.split("\t")

    category = parts[0]
    price = float(parts[1])

    if current_category == category:
        current_total += price
    else:
        if current_category is not None:
            print(f"{current_category}\t{current_total}")
        current_category = category
        current_total = price

if current_category is not None:
    print(f"{current_category}\t{current_total}")
