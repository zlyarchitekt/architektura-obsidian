import fitz
import os
import re
import shutil
import opendataloader_pdf

pdf_path = r"c:\Praca\07 BAZA WIEDZY\OBSIDIAN\Architektura\raw\RZUT34__PLEC-ayx8rw.pdf"
output_dir = r"c:\Praca\07 BAZA WIEDZY\OBSIDIAN\Architektura\RZUT-34"
chunks_dir = os.path.join(output_dir, "pdf_chunks")

os.makedirs(chunks_dir, exist_ok=True)

articles = [
    ("01_PLEC_wstepniak", 2, 5),
    ("02_100_LAT_ARCHITEKTEK", 6, 13),
    ("03_ARCHITEKTKI_NA_UCZELNIACH", 14, 23),
    ("04_BAL_ZAPRASZA_DO_TANCA_ARCHITEKTONICZKI", 24, 31),
    ("05_STABILNA_DYFUZJA_TOALET_PUBLICZNYCH", 32, 47),
    ("06_SPALCIE_TE_TECZE", 48, 56),
    ("07_KUCHENNE_REWOLUCJE", 57, 60),
    ("08_BEZPIECZENSTWO_I_HIGIENA_PRACY", 61, 77),
    ("09_WOLNA_PRZESTRZEN", 78, 89),
    ("10_SPORTPATRIARCHAT", 90, 99),
    ("11_PLEC_W_PRZESTRZENI_SYSTEMU_OCHRONY_ZDROWIA", 100, 111),
    ("12_BUDOWNICTWO_W_TKANCE_ISTNIEJACEJ", 112, 119),
    ("13_AUTORKI_I_AUTORZY", 120, 127),
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

md_files = []

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
        
        # The parser creates output file with the same base name, check what exactly
        # typically it's {title}.md
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
