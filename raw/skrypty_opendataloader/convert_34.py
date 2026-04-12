import opendataloader_pdf

try:
    print("Starting conversion...", flush=True)
    opendataloader_pdf.convert(
        input_path=["raw/RZUT34__PLEC-ayx8rw.pdf"],
        output_dir="temp_pdf_out_34/",
        format="markdown,json",
        hybrid="docling-fast",
        hybrid_mode="full"
    )
    print("Done converting RZUT34!", flush=True)
except Exception as e:
    print(f"Error during conversion: {e}", flush=True)
