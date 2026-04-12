import fitz
import os
import re
import shutil
import opendataloader_pdf

pdf_path = r"c:\Praca\07 BAZA WIEDZY\OBSIDIAN\Architektura\raw\RZUT-35-KSZTALCENIE-cdbesh.pdf"
output_dir = r"c:\Praca\07 BAZA WIEDZY\OBSIDIAN\Architektura\RZUT-35"
chunks_dir = os.path.join(output_dir, "pdf_chunks")

os.makedirs(chunks_dir, exist_ok=True)

articles = [
    ("01_ODWAGI_wstep", 2, 4),
    ("02_JEDZIEMY_NA_WYCIECZKE", 5, 12),
    ("03_POMIEDZY_DZIECKIEM_A_DOROSLYM", 13, 20),
    ("04_DOSWIADCZANIE_RZECZYWISTOSCI", 21, 28),
    ("05_SZKOLA", 29, 36),
    ("06_PRACOWAC_ZESPOLOWO", 37, 44),
    ("07_PERFEKCJA_MA_ZRODLO_W_PRAKTYCE", 45, 48),
    ("08_EDUKACJA_OBYWATELSKA", 49, 54),
    ("09_WYSILEK", 55, 60),
    ("10_NA_PRZEKOR_UTARTYM_SCIEZKOM", 61, 69),
    ("11_TUTAJ_NIE_CHODZI_O_BRYK", 70, 80),
    ("12_SPOTKANIA", 81, 86),
    ("13_AUTORZY_I_ROZMOWCY", 87, 95)
]

def clean_markdown_text(text):
    # Fix hyphenation (word-\nword -> wordword)
    text = re.sub(r'([A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+)-\s*\n+([a-ząćęłńóśźżA-ZĄĆĘŁŃÓŚŹŻ]+)', r'\1\2', text)
    # 2. Clean up spacing where line breaks happen inside a sentence
    # If a lowercase letter or comma is followed by a newline and then a lowercase letter, replace newline with space
    text = re.sub(r'([a-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ,]+)\n+([a-ząćęłńóśźż]+)', r'\1 \2', text)
    # Remove multiple spaces
    text = re.sub(r'(?<=\S) {2,}(?=\S)', ' ', text)
    return text

print("Splitting PDF...")
doc = fitz.open(pdf_path)

for title, start_page, end_page in articles:
    print(f"Processing {title}...")
    chunk_name = f"{title}.pdf"
    chunk_path = os.path.join(chunks_dir, chunk_name)
    
    # Save chunk
    chunk_doc = fitz.open()
    chunk_doc.insert_pdf(doc, from_page=start_page, to_page=end_page)
    chunk_doc.save(chunk_path)
    chunk_doc.close()
    
    # Parse to markdown using fast method
    try:
        opendataloader_pdf.convert(
            input_path=[chunk_path],
            output_dir=output_dir,
            format="markdown",
            hybrid="off"
        )
        
        md_file_path = os.path.join(output_dir, f"{title}.md")
        if os.path.exists(md_file_path):
            with open(md_file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            cleaned_content = clean_markdown_text(content)
            
            with open(md_file_path, "w", encoding="utf-8") as f:
                f.write(cleaned_content)
            print(f"    -> cleaned and saved {md_file_path}")
    except Exception as e:
        print(f"Failed to convert {title}: {e}")

print("All done!")
