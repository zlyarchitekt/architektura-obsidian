import os
import subprocess

pdf_path = "raw/RZUT34__PLEC-ayx8rw.pdf"
out_dir = "temp_pdf_out_34"

# Create output structure
os.makedirs(out_dir, exist_ok=True)

chunk_size = 16
total_pages = 128

print("Waiting a bit for hybrid server to be fully awake...")
import time
time.sleep(30)

for i in range(1, total_pages + 1, chunk_size):
    end = min(i + chunk_size - 1, total_pages)
    print(f"Processing pages {i}-{end}...")
    
    cmd_code = f"""
import opendataloader_pdf
try:
    opendataloader_pdf.convert(
        input_path=['{pdf_path}'], 
        output_dir='{out_dir}/chunk_{i}_{end}/', 
        format='markdown,json', 
        hybrid='docling-fast', 
        hybrid_mode='full', 
        pages='{i}-{end}'
    )
except Exception as e:
    print('Failed:', e)
"""
    cmd = ["python", "-c", cmd_code]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error on chunk {i}-{end}:\n", result.stderr)

print("Finished all chunks!")
