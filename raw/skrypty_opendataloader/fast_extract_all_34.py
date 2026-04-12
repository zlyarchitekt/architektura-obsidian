import opendataloader_pdf

try:
    print("Starting FAST conversion...")
    opendataloader_pdf.convert(
        input_path=["raw/RZUT34__PLEC-ayx8rw.pdf"],
        output_dir="temp_pdf_out_34_fast/",
        format="markdown,json",
        hybrid="off"
    )
    print("Done FAST converting!")
except Exception as e:
    print('Failed:', e)
