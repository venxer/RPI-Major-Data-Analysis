from globals import *
import csv

with open(FILTER_CSV, "r") as f:
    reader = csv.DictReader(f)

    for row in reader:
        # Decode AWLEVEL
        if str(int(row["AWLEVEL"])) in AWLEVEL_KEY_MAP:
            row["AWLEVEL"] = AWLEVEL_KEY_MAP[str(int(row["AWLEVEL"]))]
        # Decode MAJOR
        if row["CIPCODE"] in MAJOR_KEY_MAP:
            row["CIPCODE"] = MAJOR_KEY_MAP[row["CIPCODE"]]

        with open(DECODED_CSV, "a") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            if outfile.tell() == 0:
                writer.writeheader()
            writer.writerow(row)
