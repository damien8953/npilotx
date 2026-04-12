import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

def get_atis(icao_code):
    url = f"https://atis.guru/atis/{icao_code}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        atis_blocks = soup.find_all('div', class_='atis')
        
        output = ""
        for block in atis_blocks:
            lines = [line.strip() for line in block.get_text(separator='\n').split('\n') if line.strip()]
            content = "\n".join(lines)
            
            junk = ["METAR", "TAF", "SPECI"]
            if any(k in content.upper() for k in junk):
                continue
            
            if len(content) > 10:
                output += f"{content}\n" + "-"*20 + "\n"
        return output
    except:
        return ""

def save_to_file(icao, data, timestamp):
    # 這裡只處理「有數據」的情況
    if not data.strip():
        print(f"⏭️ {icao} 無效數據，跳過存檔以保留舊資料。")
        return False

    filename = f"atis_{icao}.txt"
    file_content = f"✈️ {icao} ATIS MONITOR\n"
    file_content += f"更新時間: {timestamp}\n"
    file_content += "==============================\n\n"
    file_content += data
        
    with open(filename, "w", encoding="utf-8") as f:
        f.write(file_content)
    print(f"✅ {filename} 已更新！")
    return True

if __name__ == "__main__":
    airports = ["VHHH", "ZSAM", "RCKH", "RCTP", "WSSS"]
    retry_list = []

    # 取得香港時間
    now_hk = datetime.utcnow() + timedelta(hours=8)
    timestamp = now_hk.strftime("%Y-%m-%d %H:%M:%S")

    print(f"🚀 第一輪抓取開始...")
    for icao in airports:
        data = get_atis(icao)
        if data.strip():
            save_to_file(icao, data, timestamp)
        else:
            print(f"⚠️ {icao} 第一輪無數據。")
            retry_list.append(icao)
        time.sleep(2)

    # 重試邏輯
    if retry_list:
        print(f"\n⏳ 等待 60 秒後重試失敗的機場...")
        time.sleep(60)
        
        for icao in retry_list:
            data = get_atis(icao)
            if data.strip():
                save_to_file(icao, data, timestamp)
            else:
                # 關鍵點：重試失敗後，直接 print，不調用 save_to_file
                print(f"❌ {icao} 重試依然無數據，不覆蓋舊檔案。")
            time.sleep(2)
    
    print("\n🎉 任務執行完畢。")
