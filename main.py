import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def get_atis(icao_code):
    url = f"https://atis.guru/atis/{icao_code}"
    # 更加真實的瀏覽器偽裝
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        # 強制使用 utf-8 編碼
        res.encoding = 'utf-8'
        
        soup = BeautifulSoup(res.text, 'html.parser')
        atis_blocks = soup.find_all('div', class_='atis')
        
        output = ""
        for block in atis_blocks:
            # 取得所有文字並清理多餘換行
            lines = [line.strip() for line in block.get_text(separator='\n').split('\n') if line.strip()]
            content = "\n".join(lines)
            
            # 過濾垃圾關鍵字
            junk = ["METAR", "TAF", "SPECI"]
            if any(k in content.upper() for k in junk):
                continue
            
            # 只有當內容長度大於 10 個字才算有效的 ATIS
            if len(content) > 10:
                output += f"{content}\n" + "-"*20 + "\n"
        
        return output
    except Exception as e:
        return f"Fetch Error: {str(e)}\n"

if __name__ == "__main__":
    print("🚀 啟動深度抓取引擎...")
    airports = ["VHHH", "ZSAM", "RCKH", "RCTP", "WSSS"]
    
    # 取得香港時間 (UTC+8)
    # GitHub Actions 預設是 UTC，我們手動加 8 小時
    from datetime import timedelta
    now_hk = datetime.utcnow() + timedelta(hours=8)
    timestamp = now_hk.strftime("%Y-%m-%d %H:%M:%S")
    
    final_report = f"✈️ ATIS MONITOR (HKT: {timestamp})\n"
    final_report += "==============================\n\n"
    
    for icao in airports:
        print(f"正在分析 {icao}...")
        data = get_atis(icao)
        if data.strip():
            final_report += f"【 {icao} 】\n{data}\n"
        else:
            final_report += f"【 {icao} 】\n⚠️ 目前無有效 ATIS 數據。\n\n"
        time.sleep(3) # 稍微增加間隔，更有禮貌
    
    with open("atis_result.txt", "w", encoding="utf-8") as f:
        f.write(final_report)
    print("✅ 任務完成，數據已精煉。")
