import sys

current_city = None
max_price = 0.0
max_product = ""

for line in sys.stdin:
    line = line.strip()
    parts = line.split("\t")

    city = parts[0]
    price = float(parts[1])

    product = parts[2]

    if current_city == city:
        if price > max_price:
            max_price = price
            max_product = product
    else:
        if current_city is not None:
            print(f"{current_city}\t{max_price}\t{max_product}")
        current_city = city
        max_price = price
        max_product = product

if current_city is not None:
    print(f"{current_city}\t{max_price}\t{max_product}")
