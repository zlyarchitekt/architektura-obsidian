import opendataloader_pdf
import os

pdf_path = "raw/Książki/Low-Rise, High-Density Housing_.pdf"
base_name = os.path.splitext(os.path.basename(pdf_path))[0]
output_dir = os.path.join("raw/Książki", base_name)
os.makedirs(output_dir, exist_ok=True)

try:
    print("Starting conversion...", flush=True)
    opendataloader_pdf.convert(
        input_path=[pdf_path],
        output_dir=output_dir,
        format="markdown,json"
    )
    print(f"Done converting to {output_dir}!", flush=True)
except Exception as e:
    print(f"Error during conversion: {e}", flush=True)
