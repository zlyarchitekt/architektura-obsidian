import json
with open('temp_pdf_out_34_fast/RZUT34__PLEC-ayx8rw.json', encoding='utf-8') as f:
    data = json.load(f)
with open('toc.txt', 'w', encoding='utf-8') as out:
    for k in data.get('kids', []):
        t = k.get('type')
        if t in ('heading', 'paragraph'):
            text = k.get('content', '')
            # print all uppercase strings that might be titles
            if text.isupper() and len(text) > 4:
                out.write(f"Page {k.get('page number')}: {text}\n")
