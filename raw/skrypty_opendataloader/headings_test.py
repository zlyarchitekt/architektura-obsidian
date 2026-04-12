import json

with open('temp_pdf_out/RZUT-33-PLANOWANIE-b0mjya.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for k in data.get('kids', []):
    if k.get('type') == 'heading':
        print(f"{k.get('heading level')}: {k.get('content')}")
