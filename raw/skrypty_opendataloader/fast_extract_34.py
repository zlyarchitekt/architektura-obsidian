import opendataloader_pdf

try:
    opendataloader_pdf.convert(
        input_path=["raw/RZUT34__PLEC-ayx8rw.pdf"],
        output_dir="temp_pdf_out_34_fast/",
        format="json",
        pages="1-15",
        hybrid="off"
    )
except Exception as e:
    print('Failed:', e)
