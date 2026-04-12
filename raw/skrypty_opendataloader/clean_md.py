import os
import re

dir_path = 'RZUT-33'

# Known spaced-out headers
headers_map = {
    'W S T Ę P N I A K': 'WSTĘPNIAK',
    'WA RSZ AWA PR Z YSZ ŁOŚ CI B Ę DZ I E WA RSZ AWĄ N A SZ YCH M A R Z E Ń': 'WARSZAWA PRZYSZŁOŚCI BĘDZIE WARSZAWĄ NASZYCH MARZEŃ',
    'R A M Y   ROZ WOJ U': 'RAMY ROZWOJU',
    'R A M Y ROZ WOJ U': 'RAMY ROZWOJU',
    'RÓW N O U PR AW N I E N I E   WSZ YS T K I CH   U CZ E S T N I KÓW   RU CH U': 'RÓWNOUPRAWNIENIE WSZYSTKICH UCZESTNIKÓW RUCHU',
    'RÓW N O U PR AW N I E N I E WSZ YS T K I CH U CZ E S T N I KÓW RU CH U': 'RÓWNOUPRAWNIENIE WSZYSTKICH UCZESTNIKÓW RUCHU',
    'M I A S TO   JA KO   E KOS YS T E M': 'MIASTO JAKO EKOSYSTEM',
    'M I A S TO JA KO E KOS YS T E M': 'MIASTO JAKO EKOSYSTEM',
    'M Ą D R E   D O G Ę SZCZ A N I E': 'MĄDRE DOGĘSZCZANIE',
    'M Ą D R E D O G Ę SZCZ A N I E': 'MĄDRE DOGĘSZCZANIE',
    'S P O Ł ECZ N A   W R A Ż L I WOŚ Ć': 'SPOŁECZNA WRAŻLIWOŚĆ',
    'S P O Ł ECZ N A W R A Ż L I WOŚ Ć': 'SPOŁECZNA WRAŻLIWOŚĆ',
    'P O D M I E J S K I E   B I O G R A F I E': 'PODMIEJSKIE BIOGRAFIE',
    'P O D M I E J S K I E B I O G R A F I E': 'PODMIEJSKIE BIOGRAFIE',
    'N O W E S T U D I U M WA R S Z AW Y': 'NOWE STUDIUM WARSZAWY',
    'P L A N O W A N I E': 'PLANOWANIE'
}

for filename in os.listdir(dir_path):
    if not filename.endswith('.md'):
        continue
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Apply header mappings
    for bad, good in headers_map.items():
        text = text.replace(bad, good)
        
    # Replace multiple spaces with a single space (but not leading spaces / indentation if any, though markdown usually doesn't need much)
    # Be careful not to destroy markdown indentation if present.
    # We will only replace spaces between words.
    text = re.sub(r'(?<=\S) {2,}(?=\S)', ' ', text)

    # Fix words broken by hyphen + newlines: "pro-\n\ncesie" -> "procesie"
    # Matches a word character, hyphen, optional spaces, newlines, and the rest of the word
    text = re.sub(r'([A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+)-\s*\n+([a-ząćęłńóśźżA-ZĄĆĘŁŃÓŚŹŻ]+)', r'\1\2', text)
    
    # Fix paragraphs broken in the middle of a sentence.
    # It finds a letter/comma followed by 1 or 2 newlines, and then a lowercase letter.
    text = re.sub(r'([a-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ,])\n+([a-ząćęłńóśźż])', r'\1 \2', text)

    # Sometimes PDF parser splits a word literally by space across line: "roz" \n "wiązywaniu"
    # This is harder to catch without a dictionary.
    # Let's write back
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

print("Korekta zrobiona.")
