import re
import json

INPUT_FILE = 'index.txt'
OUTPUT_FILE = 'drive_ids.json'

# Pola regex untuk mengambil drive ID yang diawali dengan angka 1, diikuti oleh huruf, angka, _ atau -
pattern = re.compile(r'^(1[\w-]+)\.')

results = []

with open(INPUT_FILE, 'r') as infile:
    for line in infile:
        if not line.strip():
            continue
        # Ambil token pertama sebagai nama file
        filename = line.strip().split()[0]
        match = pattern.match(filename)
        if match:
            drive_id = match.group(1)
        else:
            drive_id = None
        results.append({
            "filename": filename,
            "gdrive_id": drive_id
        })

with open(OUTPUT_FILE, 'w') as outfile:
    json.dump(results, outfile, indent=2)

print(f"Drive ID berhasil disimpan ke {OUTPUT_FILE}")
