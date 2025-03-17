import json
import requests
import sys

INPUT_FILE = 'drive_ids.json'
OUTPUT_FILE = 'drive_files.json'

# Ganti dengan API key Google Anda
API_KEY = 'AIzaSyBIeFJBYcbR3vmidklYyQtXFp4zXmveY4Q'

def main():
    # Baca daftar objek dari file JSON input
    with open(INPUT_FILE, 'r') as f:
        items = json.load(f)
    
    total = len(items)
    success_count = 0
    error_count = 0

    # Buka file output dan tulis pembuka array JSON
    with open(OUTPUT_FILE, 'w') as out:
        out.write('[\n')
        out.flush()  # pastikan pembuka sudah ditulis

        for i, item in enumerate(items):
            filename = item.get("filename")
            fileid = item.get("gdrive_id")
            url = f'https://www.googleapis.com/drive/v3/files/{fileid}?fields=name&key={API_KEY}'
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    fileoriname = data.get("name", "UNKNOWN")
                    success_count += 1
                else:
                    print(f"Error retrieving metadata for {fileid}: {response.text}")
                    fileoriname = None
                    error_count += 1
            except Exception as e:
                print(f"Exception for {fileid}: {e}")
                fileoriname = None
                error_count += 1

            # Buat objek output dengan format yang diinginkan
            new_item = {
                "filename": filename,
                "fileid": fileid,
                "fileoriname": fileoriname
            }
            
            # Tulis hasil secara langsung ke file dan flush
            json.dump(new_item, out, indent=2)
            if i < total - 1:
                out.write(',\n')
            else:
                out.write('\n')
            out.flush()

            # Tampilkan progress di terminal
            progress = (i + 1) / total * 100
            print(f"Processing {i + 1}/{total} ({progress:.2f}%) - {fileid} | Sukses: {success_count}, Error: {error_count}")
            sys.stdout.flush()
        
        # Tutup array JSON
        out.write(']\n')
        out.flush()
    
    print(f"\nProses selesai. Total: {total} | Sukses: {success_count} | Gagal: {error_count}")
    
if __name__ == '__main__':
    main()
