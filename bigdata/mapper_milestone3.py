import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split("\t")

    time_str = fields[1]
    parts = time_str.split(":")
    hour = int(parts[0])
    minute = int(parts[1])

    if (hour == 9 and minute >= 1) or (hour == 10 and minute == 0):
        print(f"09:01-10:00\t1")
    elif (hour == 10 and minute >= 1) or (hour == 11 and minute == 0):
        print(f"10:01-11:00\t1")
