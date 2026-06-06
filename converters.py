from pdf2docx import Converter
import subprocess
import os


def word_to_pdf(input_file, output_file):
    """
    Convert DOCX to PDF using LibreOffice
    """

    output_dir = os.path.dirname(output_file)

    if not output_dir:
        output_dir = "."

    os.makedirs(output_dir, exist_ok=True)

    subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            input_file,
            "--outdir",
            output_dir,
        ],
        check=True,
    )

    # LibreOffice creates PDF with same name as input file
    generated_pdf = os.path.join(
        output_dir,
        os.path.splitext(os.path.basename(input_file))[0] + ".pdf"
    )

    # Rename if output filename is different
    if generated_pdf != output_file:
        os.replace(generated_pdf, output_file)


def pdf_to_word(input_file, output_file):
    """
    Convert PDF to DOCX
    """

    converter = Converter(input_file)

    try:
        converter.convert(output_file, start=0, end=None)
    finally:
        converter.close()