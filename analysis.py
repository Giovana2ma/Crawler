import pandas as pd
import json
import re

def read_debug_log(file_path):
    records = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Try to extract the JSON part
            match = re.search(r'(\{.*\})', line)
            if match:
                json_str = match.group(1)
                try:
                    record = json.loads(json_str)
                    records.append(record)
                except json.JSONDecodeError:
                    pass  # Ignore bad lines

    df = pd.DataFrame(records)
    return df

df = read_debug_log("saida.txt")
print(df['title'][0])