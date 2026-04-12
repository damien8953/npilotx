import requests
from bs4 import BeautifulSoup
import time
import sys
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
            if any(k in content.upper() for k in ["METAR", "TAF", "SPECI"]): continue
            if len(content) > 10:
                output += f"{content}\n" + "-"*20 + "\n"
        return output
    except:
        return ""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("缺少機場參數")
        sys.exit(1)
    
    icao = sys.argv[1].upper()
    now_hk = datetime.utcnow() + timedelta(hours=8)
    timestamp = now_hk.strftime("%Y-%m-%d %H:%M:%S")

    print(f"🚀 啟動獨立任務: {icao} (最大重試次數: 10)")

    # 迴圈改為 1 到 10 次
    for attempt in range(1, 11):
        data = get_atis(icao)
        if data.strip():
            filename = f"atis_{icao}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"✈️ {icao} ATIS MONITOR\nUpdate: {timestamp}\n"+"="*30+"\n\n"+data)
            print(f"✅ {icao} 更新成功 (第 {attempt} 次嘗試)")
            sys.exit(0)
        else:
            if attempt < 10:
                print(f"⚠️ {icao} 失敗，30秒後重試 ({attempt}/10)...")
                time.sleep(30)
            else:
                print(f"❌ {icao} 已達 10 次重試上限，放棄本次更新。")
