import os
import json

def combine():
    combined_data = {}
    print("Searching for ATIS files...")
    # 遍歷當前目錄下所有的 atis_XXXX.txt
    count = 0
    for filename in os.listdir('.'):
        if filename.startswith("atis_") and filename.endswith(".txt"):
            icao = filename[5:9].upper()
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    combined_data[icao] = f.read()
                    count += 1
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    # 寫入成一個 JSON 檔案
    with open("all_atis.json", "w", encoding="utf-8") as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Combined {count} airports into all_atis.json")

if __name__ == "__main__":
    combine()
