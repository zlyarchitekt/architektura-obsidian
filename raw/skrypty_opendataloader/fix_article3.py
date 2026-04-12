import os
import re
import subprocess
import time
import opendataloader_pdf

pdf_path = r"c:\Praca\07 BAZA WIEDZY\OBSIDIAN\Architektura\RZUT-33\pdf_chunks\03_WARSZAWA_PRZYSZLOSCI_BEDZIE_WARSZAWA_NASZYCH_MARZEN.pdf"
output_dir = r"c:\Praca\07 BAZA WIEDZY\OBSIDIAN\Architektura\RZUT-33"
title = "03_WARSZAWA_PRZYSZLOSCI_BEDZIE_WARSZAWA_NASZYCH_MARZEN"

def clean_markdown_text(text):
    text = re.sub(r'([A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+)-\s*\n+([a-ząćęłńóśźżA-ZĄĆĘŁŃÓŚŹŻ]+)', r'\1\2', text)
    text = re.sub(r'([a-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ,]+)\n+([a-ząćęłńóśźż]+)', r'\1 \2', text)
    text = re.sub(r'(?<=\S) {2,}(?=\S)', ' ', text)
    return text

print("Starting hybrid server...")
server_process = subprocess.Popen(
    ["opendataloader-pdf-hybrid", "--port", "5002", "--enrich-picture-description"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    shell=True # Shell true to resolve command on windows
)

print("Waiting 30 seconds for the server to load models...")
time.sleep(30)

print(f"Parsing {title} in hybrid mode...")
try:
    opendataloader_pdf.convert(
        input_path=[pdf_path],
        output_dir=output_dir,
        format="markdown",
        hybrid="docling-fast",
        hybrid_mode="full"
    )
    
    md_file_path = os.path.join(output_dir, f"{title}.md")
    if os.path.exists(md_file_path):
        with open(md_file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        cleaned_content = clean_markdown_text(content)
        
        with open(md_file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_content)
        print(f"-> cleaned and saved {md_file_path}")
except Exception as e:
    print(f"Failed to convert {title}: {e}")

print("Terminating server...")
# Special kill needed on windows if shell=True is used
subprocess.run(["taskkill", "/F", "/T", "/PID", str(server_process.pid)])
print("All done!")
