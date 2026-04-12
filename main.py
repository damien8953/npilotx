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
    except Exception as e:
        return f"Fetch Error: {str(e)}\n"

if __name__ == "__main__":
    airports = ["VHHH", "ZSAM", "RCKH", "RCTP", "WSSS"]
    
    # 取得香港時間 (UTC+8)
    now_hk = datetime.utcnow() + timedelta(hours=8)
    timestamp = now_hk.strftime("%Y-%m-%d %H:%M:%S")
    
    for icao in airports:
        print(f"正在處理 {icao}...")
        data = get_atis(icao)
        
        # 準備該機場的內容
        file_content = f"✈️ {icao} ATIS MONITOR\n"
        file_content += f"更新時間: {timestamp}\n"
        file_content += "==============================\n\n"
        
        if data.strip():
            file_content += data
        else:
            file_content += "⚠️ 目前無有效 ATIS 數據。\n"
            
        # 關鍵修改：為每個機場建立獨立檔案
        filename = f"atis_{icao}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(file_content)
        
        print(f"✅ {filename} 已更新")
        time.sleep(2)
