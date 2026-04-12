import fitz
import os
import re
import shutil
import opendataloader_pdf

pdf_path = r"c:\Praca\07 BAZA WIEDZY\OBSIDIAN\Architektura\raw\RZUT-33-PLANOWANIE-b0mjya.pdf"
output_dir = r"c:\Praca\07 BAZA WIEDZY\OBSIDIAN\Architektura\RZUT-33"
chunks_dir = os.path.join(output_dir, "pdf_chunks")

os.makedirs(chunks_dir, exist_ok=True)

articles = [
    ("01_PLANOWANIE_wstepniak", 2, 5),
    ("02_NOWE_STUDIUM_WARSZAWY_wstep", 6, 9),
    ("03_WARSZAWA_PRZYSZLOSCI_BEDZIE_WARSZAWA_NASZYCH_MARZEN", 10, 20),
    ("04_RAMY_ROZWOJU", 21, 37),
    ("05_ROWNOUPRAWNIENIE_WSZYSTKICH_UCZESTNIKOW_RUCHU", 38, 49),
    ("06_MIASTO_JAKO_EKOSYSTEM", 50, 51),
    ("07_MADRE_DOGESZCZANIE", 52, 53),
    ("08_SPOLECZNA_WRAZLIWOSC", 54, 57),
    ("09_WYCHODZENIE_ZA_ROG", 58, 66),
    ("10_NIESCISLA_OCHRONA_PRZYRODY", 67, 87),
    ("11_SKLEBIONE_PROBLEMY_PUSTOSTANOW", 88, 101),
    ("12_PLAN_SHARONA", 102, 109),
    ("13_KRAJ_ZELBETOWYCH_GRZYBOW", 110, 115),
    ("14_PLANOWANIE_DLA_REWOLUCJI_PROGRAM_SAAL", 116, 137),
    ("15_FUNERALNE_PLANOWANIE", 138, 147),
    ("16_O_MAPACH_I_ICH_KLAMSTWACH", 148, 155),
    ("17_WIZJA_PIERWSZEGO_QUEER_MIASTX_W_PL", 156, 165),
    ("18_PODMIEJSKIE_BIOGRAFIE", 166, 175),
    ("19_AUTORZY", 176, 185)
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
