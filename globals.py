import json

RAW_DATA_DIR = "raw"
KEYS_DATA_DIR = "keys"
FILTER_DATA_DIR = "filtered_data"
FILTER_CSV = f"{FILTER_DATA_DIR}/filtered.csv"
DECODED_CSV = f"{FILTER_DATA_DIR}/decoded.csv"
AWLEVEL_KEY_MAP, COL_KEY_MAP, MAJOR_KEY_MAP = {}, {}, {}

with open(f"{KEYS_DATA_DIR}/awlevel_key.json", "r") as f:
    AWLEVEL_KEY_MAP = json.load(f)

with open(f"{KEYS_DATA_DIR}/col_key.json", "r") as f:
    COL_KEY_MAP = json.load(f)

with open(f"{KEYS_DATA_DIR}/major_key.json", "r") as f:
    MAJOR_KEY_MAP = json.load(f)