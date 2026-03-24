import sys

current_range = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    parts = line.split("\t")

    time_range = parts[0]
    count = int(parts[1])


    if current_range == time_range:
        current_count += count
    else:
        if current_range is not None:
            print(f"{current_range}\t{current_count}")
        current_range = time_range
        current_count = count

if current_range is not None:
    print(f"{current_range}\t{current_count}")
