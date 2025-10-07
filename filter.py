"""
1. Eliminate rows that do not correspond to RPI (RPI UNIT ID = 194824)
2. Eliminate rows that do not correspond to AWLEVEL values [12, 03, 05, 07]
3. Eliminate columns that begin with an "X" (e.g. "XTOTALC)
4. Aggregate data into one CSV file with an added "YEAR" column to distinguish the year of each row
"""

from pathlib import Path
import json
import re
from globals import *

for file in Path(RAW_DATA_DIR).glob("*.csv"):
    with open(file, "r") as infile:
        lines = infile.readlines()

    header = lines[0]
    header_list = header.split(",")
    omit_indices = []
    for i, col in enumerate(header_list):
        if col.startswith("X"):
            omit_indices.append(i)
    filtered_header_list = [col for i, col in enumerate(header_list) if i not in omit_indices]

    year = file.name.replace(".csv", "")

    with open(FILTER_CSV, "a") as outfile:
        # HEADER
        if outfile.tell() == 0:
            header = ",".join(["YEAR"] + filtered_header_list).encode('ascii', 'ignore').decode('ascii')
            outfile.write(header)
        for line in lines[1:]:
            # Filter by RPI UNIT ID
            if line.startswith("194824,"):
                awlevel = str(int(line.split(",")[3]))
                # Filter by AWLEVEL
                if awlevel in AWLEVEL_KEY_MAP:
                    line_list = line.split(",")
                    # Remove columns that start with "X"
                    filtered_line_list = [col for i, col in enumerate(line_list) if i not in omit_indices]
                    line = ",".join(filtered_line_list)
                    # Remove quotes from the CIPCODE column
                    line = line.replace("\"", "")

                    outfile.write(f"{year}," + line)


    print(f"Finished processing {file.name}")


