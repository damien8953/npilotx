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
    filename = f"atis_{icao}.txt"
    file_content = f"✈️ {icao} ATIS MONITOR\n"
    file_content += f"更新時間: {timestamp}\n"
    file_content += "==============================\n\n"
    
    if data.strip():
        file_content += data
    else:
        file_content += "⚠️ 目前無有效 ATIS 數據。\n"
        
    with open(filename, "w", encoding="utf-8") as f:
        f.write(file_content)
    print(f"✅ {filename} 已儲存")

if __name__ == "__main__":
    airports = ["VHHH", "ZSAM", "RCKH", "RCTP", "WSSS"]
    results = {}  # 用來存放抓取結果
    retry_list = [] # 用來存放失敗的機場

    # 取得香港時間
    now_hk = datetime.utcnow() + timedelta(hours=8)
    timestamp = now_hk.strftime("%Y-%m-%d %H:%M:%S")

    print(f"🚀 第一輪抓取開始...")
    for icao in airports:
        data = get_atis(icao)
        if data.strip():
            results[icao] = data
            save_to_file(icao, data, timestamp)
        else:
            print(f"⚠️ {icao} 暫無數據，加入重試清單。")
            retry_list.append(icao)
        time.sleep(2)

    # 如果有失敗的機場，進入重試邏輯
    if retry_list:
        print(f"\n⏳ 發現 {len(retry_list)} 個機場無數據，等待 60 秒後重試...")
        time.sleep(60)
        
        print(f"🔄 第二輪重試開始...")
        for icao in retry_list:
            data = get_atis(icao)
            if data.strip():
                print(f"✨ {icao} 重試成功！")
                save_to_file(icao, data, timestamp)
            else:
                print(f"❌ {icao} 重試後依然無數據。")
                save_to_file(icao, "", timestamp) # 最終還是沒數據就寫入提示
            time.sleep(2)
    
    print("\n🎉 任務全部完成。")
