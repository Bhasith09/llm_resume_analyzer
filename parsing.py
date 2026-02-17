# parsing.py

import io #imported to convert the uploaded file into a byte stream for PyPDF2 to read
from PyPDF2 import PdfReader #to read the pdf file and extract text from it

def extract_text_from_pdf(uploaded_file) -> str: #takes the uploaded file as input and returns the extracted text as a string
    pdf_bytes = uploaded_file.read() #reads the uploaded file 
    reader = PdfReader(io.BytesIO(pdf_bytes))#it streams  the byte data to file like object so that pypdf can read and extract text
    text = "" #created empty string to store the text after extraction
    for page in reader.pages:    #creating loop to check every text in the page so that we cosider only texts not img
        page_text = page.extract_text()  #extracting every word in the pdf page by page
        if page_text:  #if the extracted word is stext then only we are considering it
            text += page_text + "\n"  #if the word is text then storing that to text variable and adding new line after every page
    return text.strip() #using strip fn to remove any leading or trailing whitespace from the extracted text before returning it.
