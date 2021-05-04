import os
import time
import pickle   
import io
import sys
import re
from io import StringIO
from multiprocessing import Pool
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.high_level import extract_text

# Define a function to parse pdf 
def parse_pdf(file_name, page_sep=False):
    '''Return text of a pdf file
    
    Args:
        file_name (str): a string of the file name.
        page_sep (bool): return all text as a string if False, 
                         a list of text on each page if True.
    '''
    # Set up pdf parsing environment
    output_string = StringIO()
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Determine the number of pages in the file 
    fp = open(file_name, 'rb')
    length = len(list(PDFPage.get_pages(fp)))

    # Determine the start of meeting 
    # for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
    #     interpreter.process_page(page)
    #     content = retstr.getvalue().replace('\n', ' ').replace('  ', ' ').replace('\x0c', '')
    #     retstr.truncate(0)
    #     retstr.seek(0)
    #     if re.search("pengerusi", content): # where the meeting started 
    #         start_no = pageNumber
    #         print(file_name, start_no)
    #         break

    # if 'start_no' in locals():
    #     page_no = range(start_no, length) 
    # else:
    #     print("Starting page not found", file_name)
    #     return None

    # yet to determine a keyword that can determine the start in all files 

    page_no = range(0, length) 
    
    # Read data
    if page_sep == False: 
        # Get all text in the file as a string 
        text = extract_text(file_name, page_numbers = page_no)
    elif page_sep == True:     
        # Separate the content of each page and store in a list 
        text = []
        for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
            if pageNumber in page_no:
                interpreter.process_page(page)
                text.append(retstr.getvalue().replace('\n', ' ').replace('  ', ' ').replace('\x0c', ''))
                retstr.truncate(0)
                retstr.seek(0)    
    return [file_name, text] 

if __name__ == '__main__':

    folder = sys.argv[1]
    os.chdir("data/" + folder)
    files = os.listdir()

    start = time.time()
    pool = Pool()
    data = pool.map(parse_pdf, files)
    pickle.dump(data, open("../pickle/hansard_" + folder, "wb"))
    pool.close()
    pool.join()

    print("done", time.time()-start)