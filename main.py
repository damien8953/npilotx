import requests
from bs4 import BeautifulSoup
import time

def get_atis(icao_code, max_retries=5):
    url = f"https://atis.guru/atis/{icao_code}"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, 'html.parser')
            atis_blocks = soup.find_all('div', class_='atis')
            
            valid_atis_found = False
            if atis_blocks:
                print(f"--- {icao_code} 數據內容 ---")
                for block in atis_blocks:
                    content = block.get_text(separator='\n').strip()
                    # 過濾垃圾文字
                    if "METAR" in content.upper() or "TAF" in content.upper():
                        continue
                    if content:
                        print(content)
                        print("-" * 20)
                        valid_atis_found = True
            
            if valid_atis_found:
                return True
        except Exception:
            pass
        time.sleep(2)
    return False

if __name__ == "__main__":
    airport_list = ["VHHH", "ZSAM", "RCKH", "RCTP", "WSSS"]
    for icao in airport_list:
        get_atis(icao)
        time.sleep(2)
