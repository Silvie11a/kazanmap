import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://kazanbusonline.ru/1"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

stop_block = soup.find(string="Остановки:")
stops_list = []

if stop_block:
    next_elem = stop_block.parent.next_sibling
    while next_elem:
        if hasattr(next_elem, 'name') and next_elem.name == 'br':
            pass 
        elif hasattr(next_elem, 'string') and next_elem.string:
            text = next_elem.string.strip()
            if text:  
                stops_list.append(text)
        elif hasattr(next_elem, 'name') and next_elem.name in ['ul', 'ol']:
            for li in next_elem.find_all('li'):
                text = li.get_text(strip=True)
                if text:
                    stops_list.append(text)
        next_elem = next_elem.next_sibling

if not stops_list:
    all_text = soup.get_text()
    start_idx = all_text.find("Остановки:")
    if start_idx != -1:
        rest = all_text[start_idx + len("Остановки:"):].strip()
        lines = [line.strip() for line in rest.splitlines() if line.strip()]
        stops_list = lines
stops_list = [s for s in stops_list if s]

data = {
    "номер маршрута": ["1"] * len(stops_list),
    "тип транспортного средства": ["автобус"] * len(stops_list),
    "название остановки": stops_list,
    "id остановки": [f"stop_{i+1}" for i in range(len(stops_list))],
    "номер по счёту": list(range(1, len(stops_list) + 1))
}

df = pd.DataFrame(data)

df.to_csv("маршрут_1.csv", index=False, encoding='utf-8-sig')

print(f"✅ Готово! Найдено {len(stops_list)} остановок.")
print("Файл сохранён как 'маршрут_1.csv'")
print("\nПервые 5 строк:")
print(df.head().to_string(index=False))
