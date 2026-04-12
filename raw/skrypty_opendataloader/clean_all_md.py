import pathlib
import re

dirs = ['RZUT-33', 'RZUT-34', 'RZUT-35']
base = pathlib.Path(r'c:\Praca\07 BAZA WIEDZY\OBSIDIAN\Architektura')

count = 0
for d in dirs:
    for f in (base / d).glob('*.md'):
        text = f.read_text(encoding='utf-8')
        new_lines = [l for l in text.splitlines(True) if l.strip() != '!']
        new_text = ''.join(new_lines)
        new_text = re.sub(r'\n{3,}', '\n\n', new_text)
        
        if text != new_text:
            f.write_text(new_text, encoding='utf-8')
            count += 1
            print(f"Cleaned {f.name}")

print(f'\nCleaned {count} files in total.')
