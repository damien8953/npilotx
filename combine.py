import os
import json

def combine():
    combined_data = {}
    # 掃描當前目錄下所有的 atis_XXXX.txt
    for filename in os.listdir('.'):
        if filename.startswith("atis_") and filename.endswith(".txt"):
            icao = filename[5:9].upper()
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    combined_data[icao] = f.read()
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    # 寫入成一個 JSON 檔案
    with open("all_atis.json", "w", encoding="utf-8") as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
    print("✅ all_atis.json created successfully!")

if __name__ == "__main__":
    combine()
