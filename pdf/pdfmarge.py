import PyPDF2
import os

def merge_pdfs(pdf_list, output):
    pdf_writer = PyPDF2.PdfWriter()

    for pdf in pdf_list:
        pdf_reader = PyPDF2.PdfReader(pdf)
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

    with open(output, 'wb') as out:
        pdf_writer.write(out)

# Directory containing the PDFs
directory = 'files'

# List of PDFs to merge
pdfs = [os.path.join(directory, f'{i}.pdf') for i in range(1, len(os.listdir(directory)) + 1)]

# Output PDF
output_pdf = 'merged.pdf'

merge_pdfs(pdfs, output_pdf)