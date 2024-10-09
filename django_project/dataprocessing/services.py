import fitz  # PyMuPDF

def extract_pdf_data(file_path):
    pdf_document = fitz.open(file_path)
    text = ""
    
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    pdf_document.close()
    return text
