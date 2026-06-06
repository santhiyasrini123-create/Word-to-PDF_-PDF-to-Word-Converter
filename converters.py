from pdf2docx import Converter
from docx2pdf import convert
import subprocess
import os

def word_to_pdf(input_file, output_file):

    output_dir = os.path.dirname(output_file)

    subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            input_file,
            "--outdir",
            output_dir
        ],
        check=True
    )


def pdf_to_word(input_file, output_file):
    """
    Convert PDF to DOCX
    """
    cv = Converter(input_file)

    try:
        cv.convert(output_file)
    finally:
        cv.close()