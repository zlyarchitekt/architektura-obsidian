import re

try:
    with open('temp_pdf_out/RZUT-33-PLANOWANIE-b0mjya.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    titles = []
    for line in lines:
        line = line.strip()
        if line == 'W S T Ę P N I A K':
            titles.append(line)
        elif line.startswith('# ') and 'RZUT' not in line:
            titles.append(line)
        elif line.startswith('## ') and line != '## ~':
            titles.append(line)

    for i, t in enumerate(titles):
        print(i, t)
except Exception as e:
    print(f"Error: {e}")
