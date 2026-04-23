import opendataloader_pdf
import os

pdf_path = "raw/tehpublicationmanifestoofthirdlandscape145x225mm2022webspreads.pdf"
out_dir = "temp_third_landscape"
os.makedirs(out_dir, exist_ok=True)

print(f"Converting: {pdf_path}")
try:
    opendataloader_pdf.convert(
        input_path=[pdf_path],
        output_dir=out_dir,
        format="markdown",
        hybrid="off"
    )
    print("Done.")
except Exception as e:
    print(f"Failed: {e}")
    raise
