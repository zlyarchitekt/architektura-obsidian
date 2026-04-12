import fitz
import os
import subprocess
import time

pdf_path = "raw/RZUT34__PLEC-ayx8rw.pdf"
out_dir = "temp_pdf_out_34/parts"
os.makedirs(out_dir, exist_ok=True)

# 1. Start the hybrid server
print("Starting hybrid server...")
server_process = subprocess.Popen(
    ["opendataloader-pdf-hybrid", "--port", "5002", "--enrich-picture-description"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
# give it plenty of time to load models
time.sleep(30)

# 2. Split PDF
print("Splitting PDF into smaller chunks...")
doc = fitz.open(pdf_path)
chunk_size = 15
num_pages = len(doc)

part_files = []
for start_i in range(0, num_pages, chunk_size):
    end_i = min(start_i + chunk_size, num_pages) - 1
    part_doc = fitz.open()
    part_doc.insert_pdf(doc, from_page=start_i, to_page=end_i)
    part_name = f"part_{start_i+1:03d}_{end_i+1:03d}.pdf"
    part_path = os.path.join(out_dir, part_name)
    part_doc.save(part_path)
    part_files.append(part_path)
    part_doc.close()

# 3. Parse each part
final_dir = "RZUT-34"
os.makedirs(final_dir, exist_ok=True)

print("Parsing chunks...")
for p in part_files:
    print(f"Converting {p}...")
    cmd_code = f"""
import opendataloader_pdf
try:
    opendataloader_pdf.convert(
        input_path=['{p}'], 
        output_dir='{final_dir}', 
        format='markdown,json', 
        hybrid='docling-fast', 
        hybrid_mode='full'
    )
except Exception as e:
    print('Failed:', e)
"""
    subprocess.run(["python", "-c", cmd_code])

# Terminate server
server_process.terminate()
print("All done!")
