import os
import re

dir_path = 'RZUT-34'

for filename in os.listdir(dir_path):
    if not filename.endswith('.md'):
        continue
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Replace multiple spaces with a single space 
    text = re.sub(r'(?<=\S) {2,}(?=\S)', ' ', text)

    # Fix words broken by hyphen + newlines: "pro-\n\ncesie" -> "procesie"
    text = re.sub(r'([A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+)-\s*\n+([a-ząćęłńóśźżA-ZĄĆĘŁŃÓŚŹŻ]+)', r'\1\2', text)
    
    # Fix paragraphs broken in the middle of a sentence.
    text = re.sub(r'([a-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ,])\n+([a-ząćęłńóśźż])', r'\1 \2', text)

    # Common RZUT 34 separated words based on standard conventions found
    text = text.replace('P Ł E Ć', 'PŁEĆ')
    text = text.replace('A U T O R K I I A U T O R Z Y', 'AUTORKI I AUTORZY')
    text = text.replace('A R C H I T E K T U R A', 'ARCHITEKTURA')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

print("Korekta RZUT-34 zrobiona.")
