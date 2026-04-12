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
        # 增加 timeout 到 15 秒，避免網路太慢導致失敗
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        atis_blocks = soup.find_all('div', class_='atis')
        
        output = ""
        for block in atis_blocks:
            lines = [line.strip() for line in block.get_text(separator='\n').split('\n') if line.strip()]
            content = "\n".join(lines)
            
            # 過濾垃圾資訊
            junk = ["METAR", "TAF", "SPECI"]
            if any(k in content.upper() for k in junk):
                continue
            
            if len(content) > 10:
                output += f"{content}\n" + "-"*20 + "\n"
        return output
    except:
        return ""

def save_to_file(icao, data, timestamp):
    filename = f"atis_{icao}.txt"
    file_content = f"✈️ {icao} ATIS MONITOR\n"
    file_content += f"更新時間: {timestamp}\n"
    file_content += "==============================\n\n"
    file_content += data
        
    with open(filename, "w", encoding="utf-8") as f:
        f.write(file_content)
    print(f"✅ {filename} 已更新！")

if __name__ == "__main__":
    airports = ["VHHH", "ZSAM", "RCKH", "RCTP", "WSSS"]
    
    # 取得香港時間 (UTC+8)
    now_hk = datetime.utcnow() + timedelta(hours=8)
    timestamp = now_hk.strftime("%Y-%m-%d %H:%M:%S")

    print(f"🚀 開始執行 ATIS 抓取任務 (每機場最多重試 5 次)...")

    for icao in airports:
        success = False
        for attempt in range(1, 6): # 1 到 5 次
            print(f"正在嘗試抓取 {icao} (第 {attempt}/5 次)...")
            data = get_atis(icao)
            
            if data.strip():
                # 抓取成功
                save_to_file(icao, data, timestamp)
                success = True
                break # 成功後跳出這個機場的重試迴圈
            else:
                if attempt < 5:
                    print(f"⚠️ {icao} 無數據，30 秒後進行第 {attempt + 1} 次重試...")
                    time.sleep(30)
                else:
                    print(f"❌ {icao} 已達 5 次重試上限，放棄本次更新，保留舊檔案。")
        
        # 每個機場處理完畢後，稍微停頓一下再換下一個機場（有禮貌的爬蟲）
        if success:
            time.sleep(2)

    print("\n🎉 所有機場處理完畢。")
