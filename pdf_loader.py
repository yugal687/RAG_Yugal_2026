import fitz

def load_pdf(pdf_path):

    pdf = fitz.open(pdf_path)

    text = ""

    for page in pdf:

        text += page.get_text()

    return text