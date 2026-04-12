import fitz
doc = fitz.open('raw/RZUT34__PLEC-ayx8rw.pdf')
with open('pages.txt', 'w', encoding='utf-8') as f:
    f.write("--- PAGE 6 ---\n")
    f.write(doc[6].get_text())
    f.write("\n--- PAGE 7 ---\n")
    f.write(doc[7].get_text())
