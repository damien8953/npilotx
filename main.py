import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def get_atis(icao_code):
    url = f"https://atis.guru/atis/{icao_code}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        atis_blocks = soup.find_all('div', class_='atis')
        output = ""
        for block in atis_blocks:
            content = block.get_text(separator='\n').strip()
            if "METAR" not in content.upper() and "TAF" not in content.upper() and "SPECI" not in content.upper():
                output += f"{content}\n" + "-"*20 + "\n"
        return output
    except Exception as e:
        return f"Error fetching {icao_code}: {e}\n"

if __name__ == "__main__":
    print("🚀 程式開始執行...")
    airports = ["VHHH", "ZSAM", "RCKH", "RCTP", "WSSS"]
    
    # 建立報告內容
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    final_report = f"最後更新時間: {timestamp}\n"
    final_report += "==============================\n\n"
    
    for icao in airports:
        print(f"正在抓取 {icao}...")
        final_report += f"【 {icao} 】\n"
        data = get_atis(icao)
        final_report += data if data else "⚠️ 暫無數據\n"
        final_report += "\n"
        time.sleep(2)
    
    # 強制寫入檔案
    with open("atis_result.txt", "w", encoding="utf-8") as f:
        f.write(final_report)
    
    print("✅ 檔案 atis_result.txt 已更新！")
